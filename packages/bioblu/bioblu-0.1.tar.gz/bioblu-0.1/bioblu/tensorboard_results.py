#!/usr/bin/env python3

import os
import tensorboard


def show_results(fpath):
    os.system(f"tensorboard --logdir={fpath}")


if __name__ == '__main__':
    FPATH = '/media/findux/DATA/Documents/Malta_II/radagast_transport/3303_2022-02-07_201522_on_dataset_01/'
    show_results(FPATH)

    # then open http://localhost:6006/ in browser.