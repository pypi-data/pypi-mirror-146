#!/usr/bin/env python3

import json
import logging
import numpy as np
import os
import pandas as pd
from PIL import Image, UnidentifiedImageError
import random
import shutil
from typing import List, Tuple, Dict, Union

from bioblu.ds_manage import ds_annotations
from bioblu.ds_manage import ds_split
from bioblu.ds_manage import bbox_conversions


YOLO_IMG_FORMATS = ('.bmp', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.dng', '.webp', '.mpo')


def is_valid_img(img_path) -> bool:
    try:
        img = Image.open(img_path)
    except UnidentifiedImageError:
        return False
    else:
        return True
    finally:
        img = []


def subfolders_exist(fdir) -> bool:
    _filelist = os.listdir(fdir)
    _subdirs = [elem for elem in _filelist if os.path.isdir(os.path.join(fdir, elem))]#
    return bool(_subdirs)  # Because empty lists equate to False.


def invert_dictionary(in_dict: dict) -> dict:
    """Inverts a dict (keys become values and vice versa)"""
    return {value: key for key, value in in_dict.items()}


def coco_to_yolo(coco_root_path: str,
                 yolo_target_path: str,
                 train_val_test_ratios: Tuple[float, float, float],
                 seed: int=42):
    """
    Creates a yolo-formatted dataset in the yolo_path location, from a coco-formatted dataset in the coco_path location.
    It copies the corresponding images and creates the relevant yolo annotation txt files.
    :param coco_root_path:
    :param yolo_target_path:
    :param train_val_test_ratios:
    :param seed: Default: 42.
    :return: (None).
    """
    _train_ratio, _val_ratio, _test_ratio = train_val_test_ratios
    _coco_img_path = os.path.join(coco_root_path, 'images')
    _imgs, annots = ds_annotations.load_coco_ds(coco_root_path)
    _target_directories = ds_annotations.create_yolo_directories(yolo_target_path)
    _annotations = ds_annotations.merge_img_info_into_labels(_imgs, annots)
    _annotations_new = ds_annotations.convert_df_coco_bbox_annotations_to_yolo(_annotations)
    split_names_dict = ds_split.split_instance_list_to_train_val_test(list(_annotations_new['file_name'].unique()),
                                                                      (_train_ratio, _val_ratio, _test_ratio), seed=seed)
    annotations_labelled = ds_annotations.add_set_column(_annotations_new, split_names_dict)
    ds_annotations.create_yolo_annotation_txt_files(_annotations_new, _target_directories)
    logging.info([(k, v) for k, v in _target_directories['images'].items()])
    ds_annotations.copy_image_files(_coco_img_path, _target_directories, annotations_labelled)


def add_img_dims(img_df: pd.DataFrame, img_dir):
    img_widths, img_heights = [], []
    logging.info('Extracting image dimensions')
    for i, line in img_df.iterrows():
        img_path = os.path.join(img_dir, line['img_name'])
        width, height = Image.open(img_path).size
        img_widths.append(width)
        img_heights.append(height)
    img_df['img_width'] = img_widths
    img_df['img_height'] = img_heights
    return img_df


def add_set_column(annotations: pd.DataFrame, split_dict: dict, index_column_name = 'file_name') -> pd.DataFrame:
    # ToDo: refactor this into ds_split
    """Adds a column "set" to the annotations pd.df that has the values "train", "val" and "test", depending on which set
    the corresponding image belongs to."""
    for k, v in split_dict.items():
        for _img_name in v:
            annotations.loc[annotations[index_column_name] == _img_name, 'set'] = k
    return annotations

# DEPRECATED
# def create_materials_dict(materials: List[str]):
#     """Takes a materials list and returns a dictionary with an index for each unique material: {material: index}"""
#     mats_dict = dict(enumerate(set(materials)))
#     return mats_dict


def create_yolo_annotation_line(category_id_no: int, bbox: List[float]):
    """
    Takes a cateogry id and yolo-formatted bbox coordinates and returns a string to be used in the annotation file."""
    logging.debug(category_id_no)
    logging.debug(bbox)
    category_id = str(category_id_no)
    _bbox_annotation = category_id
    for boxval in bbox:
        _bbox_annotation = ' '.join([_bbox_annotation, str(boxval)])
    return _bbox_annotation


def create_yolo_annotations(labelme_path):
    """
    Creates yolo-styled annotation files in the folder where the image and json files from labelme are located.
    :param labelme_path: path to the directory that contains image and json files.
    :param classes:
    :param train_val_test_ratio:
    :param seed:
    :return: dataframe with image and annotation info.
    """
    materials_list = extract_materials_from_labelme_jsons(labelme_path)
    materials_dict = ds_annotations.create_materials_dict_omnidirectional(set(materials_list))

    print('Starting dataframe...')
    img_list = list_image_names(labelme_path)
    json_list = list_json_names(labelme_path)
    df_joined = join_json_and_img_lists(img_list, json_list)
    df_joined = add_img_dims(df_joined, labelme_path)

    print('Creating annotation files...')
    all_annotations = []
    for i, line in df_joined.iterrows():
        annotation_file_path = os.path.join(labelme_path, line['id_name'] + '.txt')
        img_annotations = []
        if not pd.isna(line['json_name']):
            json_path = os.path.join(labelme_path, line['json_name'])
            json_file = load_json(json_path)
            for bbox in json_file['shapes']:
                points = bbox['points']
                labelme_bbox = bbox_conversions.fix_labelme_point_order(points)
                material = bbox['label']
                material_i = materials_dict[material]
                yolo_bbox = bbox_conversions.labelme_to_yolo(labelme_bbox, line['img_width'], line['img_height'])
                annotation_line = create_yolo_annotation_line(material_i, yolo_bbox)
                img_annotations.append(annotation_line + '\n')
        with open(annotation_file_path, 'w') as f:
            f.writelines(img_annotations)
        all_annotations.append(img_annotations)
    logging.info(all_annotations)
    df_joined['annotations'] = all_annotations
    return df_joined


def create_yolo_directories(target_directory: str) -> dict:
    """
    Creates the target directory, with subfolders according to yolo requirements. Also creates a "..._testing" folder in
    the parent directory.
    :param target_directory: str
    :return: dictionary with target directory paths
    """
    path_img_train = os.path.join(target_directory, 'images/train')
    path_img_val = os.path.join(target_directory, 'images/valid')
    path_img_test = os.path.join(target_directory, 'images/test')

    path_labels_train = os.path.join(target_directory, 'labels/train')
    path_labels_val = os.path.join(target_directory, 'labels/valid')
    path_labels_test = os.path.join(target_directory, 'labels/test')
    try:
        os.mkdir(target_directory)
        os.makedirs(path_img_train)
        os.makedirs(path_img_val)
        os.makedirs(path_img_test)
        os.makedirs(path_labels_train)
        os.makedirs(path_labels_val)
        os.makedirs(path_labels_test)
        print('Created directories.')
    except FileExistsError:
        raise FileExistsError('One or more target directories already exist.')
    else:
        directories = {'images': {'train': path_img_train, 'val': path_img_val, 'test': path_img_test},
                       'labels': {'train': path_labels_train, 'val': path_labels_val, 'test': path_labels_test}}
        return directories


def extract_materials_from_labelme_jsons(json_fdir) -> List[str]:
    """Returns a list of all the materials found in the json files in the target dir. May include duplicates."""
    json_files = get_paths_to_json_files(json_fdir)
    materials = []
    for json_path in json_files:
        json_data = load_json(json_path)
        for bbox in json_data['shapes']:
            materials.append(bbox['label'])
    return materials


def get_cutoff_indices(n, prop_train, prop_val, prop_test):
    assert np.isclose((prop_train + prop_val + prop_test), 1.0)
    # The following block uses int(np.round()) to prevent baker's rounding.
    _train_cutoff = int(np.round(n * prop_train))
    _val_cutoff = int(np.round(n * (prop_train + prop_val)))
    logging.debug(f'Train cutoff: {_train_cutoff}({n * prop_train})')
    logging.debug(f'Val. cutoff: {_val_cutoff}({n * (prop_train + prop_val)})')
    logging.debug(f'N - N * test_prop: {n - int(np.round(n * prop_test))}')
    assert _val_cutoff == (n - int(np.round(n * prop_test)))
    return _train_cutoff, _val_cutoff


def get_paths_to_json_files(fdir: str) -> List[str]:
    """Returns a list of paths (List[str]) to the json files found in the directory provided."""
    json_fpaths = [os.path.join(fdir, fname) for fname in sorted(os.listdir(fdir)) if fname.endswith('.json')]
    return json_fpaths


def join_json_and_img_lists(img_list: List[str], json_list: List[str]):
    """
    Joins a img and json list into a data frame with indexes.
    :param img_list:
    :param json_list:
    :return:
    """
    file_id = [fname.split('.')[0] for fname in img_list]
    # Make sure there are no duplicates (e.g. if the same image exists in two formats):
    assert len(file_id) == len(set(file_id))
    img_df = pd.DataFrame({'id_name': file_id, 'img_name': img_list}).set_index('id_name')
    json_ids = [jname.split('.')[0] for jname in json_list]
    json_df = pd.DataFrame({'id_name': json_ids, 'json_name': json_list}).set_index('id_name')
    joined_df = img_df.join(json_df, on='id_name', how='left')
    joined_df = joined_df.reset_index()
    return joined_df


def load_json(json_fpath: str) -> dict:
    """Returns json data as a dict."""
    with open(json_fpath, 'r') as f:
        data = json.load(f)
    logging.debug(f'Loaded json object (type): {type(data)}')
    return data


def list_image_names(img_dir: str) -> List[str]:
    """Returns a (sorted) list of filenames of images in a folder that can be opened by PIL.Image.open(). Note that
    they might be of various filetypes. Ignores files that can not be opened by PIL.Image.open()."""
    _files = sorted(os.listdir(img_dir))
    images = []
    for _fname_img in _files:
        try:
            _ = Image.open(os.path.join(img_dir, _fname_img))
        except UnidentifiedImageError:
            logging.info(f'{_fname_img} is not a readable image.')
        else:
            images.append(_fname_img)
    return images


def list_json_names(fdir: str) -> List[str]:
    """Returns an ordered list of all the json filenames in fdir."""
    json_fnames = [file for file in sorted(os.listdir(fdir)) if file.endswith('.json')]
    assert len(json_fnames) == len(set(json_fnames))  # Make sure fnames are unique.
    return json_fnames


def copy_yolo_files(files_df: pd.DataFrame, target_dirs: dict):
    """
    Copies images according to a dictionary that contains target directories (for train, val and test), and an
    annotations_df dataframe that has info on which image belong to which set.
    """
    files_df_reduced = files_df.drop_duplicates(subset='file_name')
    assert len(files_df_reduced['file_name']) ==\
           len(set(files_df['file_name'])) ==\
           len(set(files_df_reduced['file_name']))

    print("Copying images and annotation files...")
    for i, line in files_df.iterrows():
        _current_set = line['set']
        _img_fname = line['img_name']
        _img_source_path = line['img_fpath']
        _annotation_fname = line['annotation_name']
        _annotation_source_path = line['annotation_fpath']

        # Copy img
        _img_target_path = os.path.join(target_dirs['images'][_current_set], _img_fname)
        shutil.copyfile(_img_source_path, _img_target_path)
        # Copy annotation file
        _annot_target_path = os.path.join(target_dirs['labels'][_current_set], _annotation_fname)
        shutil.copyfile(_annotation_source_path, _annot_target_path)

    logging.info(f'Copied {i + 1} images.')
    print('Done copying.')


def create_files_dataframe(fpath: str) -> pd.DataFrame:
    """

    :param fpath:
    :return:
    """
    # Instead of the following, perhaps use a set of allowed image extensions?
    # img_files = [file for file in sorted(os.listdir(fpath)) if is_valid_img(os.path.join(fpath, file))]
    img_files = [file for file in sorted(os.listdir(fpath)) if file.endswith(YOLO_IMG_FORMATS)]
    annotation_files = [file for file in sorted(os.listdir(fpath)) if file.endswith('.txt')]
    # Verify same names:
    img_names_only = [fname.split('.')[0] for fname in img_files]
    annotation_names_only = [fname.split('.')[0] for fname in annotation_files]
    assert img_names_only == annotation_names_only
    file_dataframe = pd.DataFrame({'file_name': img_names_only,
                                   'img_name': img_files,
                                   'img_fpath': [os.path.join(fpath, imgfile) for imgfile in img_files],
                                   'annotation_name': annotation_files,
                                   'annotation_fpath': [os.path.join(fpath, annotfile) for annotfile in annotation_files]})
    return file_dataframe


def create_yolo_dataset(source_dir_path: str, target_dir_path: str,
                        instance_column_name: str = 'file_name',
                        train_val_test: Tuple = (0.6, 0.2, 0.2), seed: int = 42) -> None:
    """

    :param source_dir_path:
    :param target_dir_path:
    :param instance_column_name:
    :param train_val_test:
    :param seed:
    :return:
    """
    # use either the dataframe or the folder. think about this
    # the df needs a path column for both the images and the files. Or one general path that stops before the extension?
    files_dataframe = create_files_dataframe(source_dir_path)
    instances = list(files_dataframe[instance_column_name])
    sets = ds_split.split_instance_list_to_train_val_test(instances, prop_train_val_test=train_val_test, seed=seed)
    files_dataframe = add_set_column(files_dataframe, sets)
    target_dirs = create_yolo_directories(target_directory=target_dir_path)
    copy_yolo_files(files_dataframe, target_dirs)
    print('Yolo dataset creation complete.')


def extract_paths_to_yolo_ds_files(fpath_yolo_ds) -> Dict[str, Dict[str, list]]:
    """
    Returns a dictionary of the file paths to
    :param fpath_yolo_ds:
    :return:
    """
    train_img_dir = os.path.join(fpath_yolo_ds, "images/train")
    val_img_dir = os.path.join(fpath_yolo_ds, "images/valid")
    test_img_dir = os.path.join(fpath_yolo_ds, "images/test")

    train_labs_dir = os.path.join(fpath_yolo_ds, "labels/train")
    val_labs_dir = os.path.join(fpath_yolo_ds, "labels/valid")
    test_labs_dir = os.path.join(fpath_yolo_ds, "labels/test")

    logging.info(train_img_dir)
    logging.info(test_img_dir)
    logging.info(val_img_dir)
    logging.info(train_labs_dir)
    logging.info(test_labs_dir)
    logging.info(val_labs_dir)

    train_imgs = [os.path.join(train_img_dir, file) for file in os.listdir(train_img_dir)]
    val_imgs = [os.path.join(val_img_dir, file) for file in os.listdir(val_img_dir)]
    test_imgs = [os.path.join(test_img_dir, file) for file in os.listdir(test_img_dir)]

    train_labs = [os.path.join(train_labs_dir, file) for file in os.listdir(train_labs_dir)]
    val_labs = [os.path.join(val_labs_dir, file) for file in os.listdir(val_labs_dir)]
    test_labs = [os.path.join(test_labs_dir, file) for file in os.listdir(test_labs_dir)]

    return {"images": {"train": train_imgs,
                       "valid": val_imgs,
                       "test": test_imgs},
            "labels": {"train": train_labs,
                       "valid": val_labs,
                       "test": test_labs}}


def create_coco_json_from_yolo_set(yolo_root_dir: str, ds_set: str, target_save_file: str, materials_dict: dict = None):
    """
    Creates a json file from a yolo dataset. Using ds_set, either train, valid or test set can be specified.
    :param yolo_root_dir: Yolo root directory. Needs to have subfolders "images" and "labels", each wih subfolders "train", "test" and "valid"
    :param ds_set: Can be either "train", "test", "valid"
    :param target_save_file: json output file path
    :param materials_dict: material dict , e.g. {0: 'plastic'}
    :return:
    """
    if materials_dict is None:
        materials_dict = ds_annotations.create_fallback_yolo_materials_dict(yolo_root_dir)
    materials_dict_list = ds_annotations.create_coco_materials_dicts(materials_dict)
    inverted_mats_dict = {v: k for k, v in materials_dict.items()}
    logging.info(f"Mats dict list: {materials_dict_list}")
    logging.info(f"Mats dict: {materials_dict}")
    logging.info(f"Inv. mats dict: {inverted_mats_dict}")

    assert ds_set.lower() in ["train", "test", "valid"]

    img_dir = os.path.join(yolo_root_dir, "images", ds_set.lower())
    logging.info(f"Img dir: {img_dir}")
    labels_dir = os.path.join(yolo_root_dir, "labels", ds_set.lower())
    logging.info(f"Labels dir: {labels_dir}")

    img_paths = [os.path.join(img_dir, fname) for fname in os.listdir(img_dir)]
    labels_paths = [os.path.join(labels_dir, fname) for fname in os.listdir(labels_dir)]
    assert len(img_paths) == len(labels_paths)

    logging.info("Creating coco dict...")
    coco_dict = {"info": {"description": f"dataset created from yolo {yolo_root_dir}",
                          "year": 2022,
                          "contributor": "BIOBLU project, University of Malta"},
                 "licences": [],
                 "images": [],
                 "annotations": [],
                 "categories": materials_dict_list}

    for i, (img_path, label_path) in enumerate(zip(img_paths, labels_paths)):
        coco_dict["images"].append({"file_name": img_path,
                                    # "file_name": os.path.split(img_path)[-1],
                                    "width": Image.open(img_path).size[0],
                                    "height": Image.open(img_path).size[1],
                                    "id": i})
        yolo_boxes = ds_annotations.load_yolo_annotations(label_path, img_path, materials_dict)
        for box in yolo_boxes:
            box.to_coco()
            coco_dict["annotations"].append({"segmentation": [],
                                             "area": None,
                                             "iscrowd": 0,
                                             "image_id": i,
                                             "bbox": box.bbox,
                                             "category_id": inverted_mats_dict[box.material],
                                             "id": i})

    with open(target_save_file, "w") as f:
        json.dump(coco_dict, f, indent=4)
    logging.info(f"Coco dict saved to {target_save_file}")


def convert_yolo_to_coco(yolo_root_dir: str, coco_target_dir: str, dataset_name: str, materials_dict: dict = None) -> None:
    print("Creating coco directories and paths...")
    coco_annotations_dir = os.path.join(coco_target_dir, "annotations")
    coco_train_dir = os.path.join(coco_target_dir, dataset_name + "_train")
    coco_valid_dir = os.path.join(coco_target_dir, dataset_name + "_val")
    coco_test_dir = os.path.join(coco_target_dir, dataset_name + "_test")
    if os.path.isdir(coco_target_dir):
        raise IsADirectoryError(f"Aborted. Target dir already exists: {coco_target_dir}")
    os.makedirs(coco_target_dir)
    os.makedirs(coco_annotations_dir)
    os.makedirs(coco_train_dir)
    os.makedirs(coco_valid_dir)
    os.makedirs(coco_test_dir)

    print("Creating coco jsons...")
    if materials_dict is None:
        materials_dict = ds_annotations.create_fallback_yolo_materials_dict(yolo_root_dir)
    train_json_name = f"{coco_target_dir}/annotations/{dataset_name}_train.json"
    create_coco_json_from_yolo_set(yolo_root_dir, "train", train_json_name, materials_dict)
    valid_json_name = f"{coco_target_dir}/annotations/{dataset_name}_valid.json"
    create_coco_json_from_yolo_set(yolo_root_dir, "valid", valid_json_name, materials_dict)
    test_json_name = f"{coco_target_dir}/annotations/{dataset_name}_test.json"
    create_coco_json_from_yolo_set(yolo_root_dir, "test", test_json_name, materials_dict)

    print("Getting yolo file paths...")
    yolo_train_img_dir = os.path.join(yolo_root_dir, "images/train")
    yolo_valid_img_dir = os.path.join(yolo_root_dir, "images/valid")
    yolo_test_img_dir = os.path.join(yolo_root_dir, "images/test")
    train_img_sources = [os.path.join(yolo_train_img_dir, fname) for fname in os.listdir(yolo_train_img_dir)]
    valid_img_sources = [os.path.join(yolo_valid_img_dir, fname) for fname in os.listdir(yolo_valid_img_dir)]
    test_img_sources = [os.path.join(yolo_test_img_dir, fname) for fname in os.listdir(yolo_test_img_dir)]
    train_img_targets = [os.path.join(coco_train_dir, os.path.split(fpath)[-1]) for fpath in train_img_sources]
    valid_img_targets = [os.path.join(coco_valid_dir, os.path.split(fpath)[-1]) for fpath in valid_img_sources]
    test_img_targets = [os.path.join(coco_test_dir, os.path.split(fpath)[-1]) for fpath in test_img_sources]

    logging.debug(f"Train targets: {train_img_targets}")
    logging.debug(f"Validation targets: {valid_img_targets}")
    logging.info(f" Len train src/trg: {len(train_img_sources)}/{len(train_img_targets)}")
    logging.info(f" Len valid src/trg: {len(valid_img_sources)}/{len(valid_img_targets)}")
    logging.info(f" Len test src/trg: {len(test_img_sources)}/{len(test_img_targets)}")
    assert len(train_img_sources) == len(train_img_targets)
    assert len(valid_img_sources) == len(valid_img_targets)
    assert len(test_img_sources) == len(test_img_targets)

    print("Copying images from yolo to coco ds...")
    # Create one long sources list and one long targets list
    sources = train_img_sources
    sources.extend(valid_img_sources)
    sources.extend(test_img_sources)
    targets = train_img_targets
    targets.extend(valid_img_targets)
    targets.extend(test_img_targets)
    assert len(sources) == len(targets)

    for src, trg in zip(sources, targets):
        # Make sure it's the same file name.
        src_name = os.path.split(src)[-1]
        trg_name = os.path.split(trg)[-1]
        assert src_name == trg_name
        # Copy file
        shutil.copyfile(src, trg)
    print("Done copying image files.")


if __name__ == "__main__":
    loglevel = logging.INFO
    logformat = "[%(levelname)s]\t%(funcName)15s: %(message)s"
    logging.basicConfig(level=loglevel, format=logformat)
    # logging.disable()

    gnejna_yolo = "/media/findux/DATA/Documents/Malta_II/datasets/dataset_04_gnejna_with_duplicates/"
    gnejna_coco = "/media/findux/DATA/Documents/Malta_II/datasets/dataset_04_gnejna_with_duplicates_COCO/"
    convert_yolo_to_coco(gnejna_yolo, gnejna_coco, "gnejna")