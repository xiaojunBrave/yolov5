# -*- coding: utf-8 -*-
# @Time    : 2023/10/26 23:17
# @Author  : xiaoj
# @File    : predict.py
# @Desc    :

import detect
import glob
import json
import os

img_dir = "../pollination/data/image/"
save_dir = '../pollination/data/json/'
DataDir = "../pollination/data/time/"
def main():
    while True:
        imgs = glob.glob(img_dir + "*_bak.png")
        if imgs:
            imgbak_path = imgs[0]
            img_name = imgbak_path.split("\\")[-1][:-8]
            save_path = save_dir + img_name + '.json'
            opt = detect.parse_opt(imgbak_path)
            boxes = detect.run(**vars(opt))
            dections = {'box':boxes}
            fp = open(save_path,'w')
            json.dump(dections,fp)
            fp.close()
            os.remove(imgbak_path)
        else:
            print('No Image Received')

if __name__ == '__main__':
    main()