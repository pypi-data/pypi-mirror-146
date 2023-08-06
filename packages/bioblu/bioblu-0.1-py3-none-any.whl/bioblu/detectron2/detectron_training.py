#!/usr/bin/env python3

import cv2
import json
import logging
import numpy as np
import os
import random
from typing import List

import detectron2
from detectron2.data.datasets import register_coco_instances
from detectron2.utils.logger import setup_logger

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.structures import BoxMode
from detectron2.engine import DefaultTrainer

from detectron2.structures import BoxMode

# from bioblu.ds_manage import ds_annotations


def load_json(json_fpath: str) -> dict:
    """Returns json data as a dict."""
    with open(json_fpath, 'r') as f:
        data = json.load(f)
    logging.debug(f'Loaded json object (type): {type(data)}')
    return data


def create_detectron_img_dict_list(coco_json_fpath, bbox_format = BoxMode.XYWH_ABS) -> List[dict]:
    """
    Creates a list of dictionaries to be used in detectron2.
    :param coco_json_fpath:
    :return:
    """
    json_data = load_json(coco_json_fpath)
    images = json_data.get("images", [])
    logging.debug(f"Images: {images}")
    annotations = json_data.get("annotations", [])
    dict_list = []
    for img in images:
        current_img = {"file_name": img["file_name"],
                       "image_id": img["id"],
                       "width": img["width"],
                       "height": img["height"],
                       "annotations": []}
        for annotation in annotations:
            if annotation["image_id"] == current_img["image_id"]:
                current_img["annotations"].append({"segmentation": [],
                                                   "area": None,  # ToDo: Check if this might have to be box area.
                                                   "iscrowd": 0,
                                                   "category_id": annotation["category_id"],
                                                   "bbox_mode": bbox_format,
                                                   "bbox": annotation["bbox"]
                                                   }
                                                  )
        dict_list.append(current_img)
    return dict_list


# def fetch_img_dicts(json_path: str):
#     return create_detectron_img_dict_list(json_path)


if __name__ == "__main__":
    loglevel = logging.DEBUG
    logformat = "[%(levelname)s]\t%(funcName)15s: %(message)s"
    logging.basicConfig(level=loglevel, format=logformat)
    logging.disable()

    # Detectron2 logger
    setup_logger()

    ds_name = "mini_gnejna"
    fpath_json_train = "/opt/nfs/shared/scratch/bioblu/datasets/mini_gnejna/train/annotations.json"
    fpath_json_valid = "/opt/nfs/shared/scratch/bioblu/datasets/mini_gnejna/val/annotations.json"
    img_root_train = "/opt/nfs/shared/scratch/bioblu/datasets/mini_gnejna/train"
    img_root_train = "/opt/nfs/shared/scratch/bioblu/datasets/mini_gnejna/val"
    training_imgs = create_detectron_img_dict_list(fpath_json_train)
    validation_imgs = create_detectron_img_dict_list(fpath_json_valid)

    # validation_imgs = load_json(fpath_json_valid)["images"]
    # classes = ["trash"]
    #
    # ### COPIED FROM TUTORIAL:
    # cfg = get_cfg()
    #
    # DatasetCatalog.register("category_train", lambda: fetch_img_dicts(fpath_json_train))
    # MetadataCatalog.get("category_train").set(thing_classes=["trash"])
    # DatasetCatalog.register("category_val", lambda: fetch_img_dicts(fpath_json_train))
    # MetadataCatalog.get("category_val").set(thing_classes=["trash"])
    # logging.info("Instances registered.")
    # microcontroller_metadata = MetadataCatalog.get("category_train")
    #
    # cfg.DATASETS.TRAIN = ("mini_gnejna_train",)
    # cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_C4_1x.yaml"))
    # logging.debug("Merged from model zoo.")
    # cfg.DATASETS.TEST = ("mini_gnejna_val",)
    # cfg.DATALOADER.NUM_WORKERS = 2
    # cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_C4_1x.yaml")  # Let training initialize from model zoo
    # logging.debug("Loaded weights from zoo.")
    # cfg.SOLVER.IMS_PER_BATCH = 2
    # cfg.SOLVER.BASE_LR = 0.00025  # pick a good LR
    # cfg.SOLVER.MAX_ITER = 1200    # 300 iterations seems good enough for the tutorial dataset; you will need to train longer for a practical dataset
    # cfg.SOLVER.STEPS = []        # do not decay learning rate
    # cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128   # faster, and good enough for this toy dataset (default: 512)
    # cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1  # only has one class (ballon). (see https://detectron2.readthedocs.io/tutorials/datasets.html#update-the-config-for-new-datasets)
    # # NOTE: this config means the number of classes, but a few popular unofficial tutorials incorrect uses num_classes+1 here.
    #
    # os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    # logging.debug("Created output dir.")
    # trainer = DefaultTrainer(cfg)
    # logging.debug("Set up trainer.")
    # trainer.resume_or_load(resume=False)
    # logging.debug("Starting training.")
    # trainer.train()

    json_fpath = "/media/findux/DATA/Documents/Malta_II/datasets/dataset_04_gnejna_with_duplicates_COCO/annotations/gnejna_train.json"
    ds_annotations.save_readable_json(json_fpath, "/home/findux/Desktop/gnejna_train.json")
    img_dict_list = create_detectron_img_dict_list(json_fpath)
    ds_annotations.save_to_json(img_dict_list, "/home/findux/Desktop/img_dict_list.json")


