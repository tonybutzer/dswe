#!/usr/bin/env python
# coding: utf-8

from stacLib.ard_stac_search import Astac
import rasterio as rio
from rasterio.windows import Window

import sys
import os
import numpy as np
import random
#import tqdm.notebook as tq
import tqdm as tq
import zarr

os.environ['AWS_REQUEST_PAYER']='requester'

BUCKET = 'dev-nlcd-developer'


# file_path = 'dancecard.txt'  # Replace 'your_file.txt' with the actual path to your text file

# def get_text_from_line(file_path, line_number):
    # with open(file_path, 'r') as file:
        # lines = file.readlines()
        # if 1 <= line_number <= len(lines):
            # return lines[line_number - 1]
        # else:
            # return f"Line number {line_number} is out of range."


# Get the text from the randomly chosen line
# def get_my_work_from(task_number):
    # random_line_number = task_number
    # random_line_text = get_text_from_line(file_path, random_line_number)
# 
    # print(f"Random Line Number: {random_line_number}")
    # print(f"Text from Line {random_line_number}: {random_line_text}")
    # work = random_line_text.rstrip()
    # return work


# https://landsat.usgs.gov/ard_tile
#work = 'H21V10_Y18X7'
work = 'H16V04_Y10X14'

#work = sys.argv[1]


def get_work(work_str):
    
    next = work_str.split('X')[0]
    X = work_str.split('X')[1]
    #print(next, X)
    Y = next.split('Y')[1]
    nex = next.split('Y')[0]
    ne, V_ = nex.split('V')
    V = V_.replace('_','')
    H = ne.replace('H','')
    #print(H,V,Y,X)
    return (H,V,Y,X)
    


#my_date='2021-01-01/2021-12-31'
my_date='1997-01-01/1997-12-31'


stac_config = {}

stac_config['url'] = 'https://landsatlook.usgs.gov/stac-server'
stac_config['fav_collection'] = 'landsat-c2l3-dswe'
stac_config['description'] = 'Landsat Collection 2 ARD Tiles DSWE'


print(work)
(H,V,Y,X) = get_work(work)


print(H,V,Y,X)


chunkY = 250
chunkX = 250


_stac = Astac(stac_config)


date_range_text = my_date
cloud_cover_pct_max = '100'
_assets = _stac.get_my_assets(None, H, V, date_range_text, cloud_cover_pct_max)


print(_assets[0]['properties'])


def read_tif(path: str, band: int = 1, window: Window = None):
    return rio.open(path).read(band, window=window)

def read_ls_data(item, band, window):
    return read_tif(item['assets'][band]['alternate']['s3']['href'], window=window)


len(_assets)


# Initialize 3d array time Y X

yoff = int(Y) * chunkY
xoff = int(X) * chunkX

# Note col row - is opposite of C-style numpy arrays
# Window(col_off, row_off, width, height)

window = Window(xoff, yoff, chunkX, chunkY)


big3d_ary = np.zeros(shape=(len(_assets), chunkY, chunkX), dtype=np.uint16)


print(big3d_ary.shape)


p_bar=tq.tqdm(range(len(_assets)), position=0, leave=True)
myband='intsm'
for t1 in range(len(_assets)):
    item = _assets[t1]
    big3d_ary[t1] = read_ls_data(item, myband, window)
    p_bar.update(1)
    p_bar.refresh()


Z_store = f's3://{BUCKET}/dswe/v0/{myband}/_H{H}V{V}_Y{Y}X{X}_store.zarr'


# Save the 3D NumPy array as a Zarr array
print('SAVING ... ', Z_store)
zarr.save(Z_store, big3d_ary)

big3d_ary = np.zeros(shape=(len(_assets), chunkY, chunkX), dtype=np.uint16)


print(big3d_ary.shape)


p_bar=tq.tqdm(range(len(_assets)), position=0, leave=True)
myband='diag'
for t1 in range(len(_assets)):
    item = _assets[t1]
    big3d_ary[t1] = read_ls_data(item, myband, window)
    p_bar.update(1)
    p_bar.refresh()


Z_store = f's3://{BUCKET}/dswe/v0/{myband}/_H{H}V{V}_Y{Y}X{X}_store.zarr'


# Save the 3D NumPy array as a Zarr array
print('SAVING ... ', Z_store)
zarr.save(Z_store, big3d_ary)




