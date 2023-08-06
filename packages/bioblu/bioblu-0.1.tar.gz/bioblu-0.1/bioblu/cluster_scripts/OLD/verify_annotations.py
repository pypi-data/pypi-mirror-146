import logging
import pandas as pd

from bioblu.ds_manage import ds_annotations

pd.options.display.max_columns = 10
logging.basicConfig(level=logging.DEBUG, format="%(message)s")
logging.disable()

imgs, annots = ds_annotations.load_coco_ds("/opt/local/data/rpfei01/datasets/UAVVaste")
annotations_merged = ds_annotations.merge_img_info_into_labels(imgs, annots)

img_dir = "/opt/local/data/rpfei01/datasets/UAVVaste/images"

ds_annotations.show_img_annotations_coco("GOPR0049.JPG", img_dir, annotations_merged)
ds_annotations.show_all_annotations_coco(img_dir, annotations_merged)