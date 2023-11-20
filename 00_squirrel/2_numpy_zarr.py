#!/usr/bin/env python
# coding: utf-8

get_ipython().run_line_magic('env', 'AWS_REQUEST_PAYER=requester')


from stacLib.ard_stac_search import Astac
import rasterio as rio
from rasterio.windows import Window

import numpy as np
import tqdm.notebook as tq
import zarr


work = 'H21V10_Y18X7'


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
    


my_date='2020-01-01/2024-12-31'


stac_config = {}

stac_config['url'] = 'https://landsatlook.usgs.gov/stac-server'
stac_config['fav_collection'] = 'landsat-c2l3-dswe'
stac_config['description'] = 'Landsat Collection 2 ARD Tiles DSWE'


print(work)
(H,V,Y,X) = get_work(work)


(H,V,Y,X)


chunkY = 250
chunkX = 250


_stac = Astac(stac_config)


date_range_text = my_date
cloud_cover_pct_max = '100'
_assets = _stac.get_my_assets(None, H, V, date_range_text, cloud_cover_pct_max)


_assets[0]['properties']


def read_tif(path: str, band: int = 1, window: Window = None):
    return rio.open(path).read(band, window=window)

def read_ls_data(item, band, window):
    return read_tif(item['assets'][band]['alternate']['s3']['href'], window=window)


len(_assets)


# Initialize 3d array time Y X


window = Window(0, 0, chunkY, chunkX)


big3d_ary = np.zeros(shape=(len(_assets), chunkY, chunkX), dtype=np.uint16)


big3d_ary.shape


get_ipython().run_cell_magic('time', '', "p_bar=tq.tqdm(range(len(_assets)), position=0, leave=True)\nmyband='intsm'\nfor t1 in range(len(_assets)):\n    item = _assets[t1]\n    big3d_ary[t1] = read_ls_data(item, myband, window)\n    p_bar.update(1)\n    p_bar.refresh()\n")


Z_store = f's3://ws-out/dwse/_H{H}V{V}_Y{Y}X{X}_store.zarr'


get_ipython().run_cell_magic('time', '', '# Save the 3D NumPy array as a Zarr array\nzarr.save(Z_store, big3d_ary)\n')




