#!/usr/bin/env python
# coding: utf-8

# In[56]:


import sys
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
import glob
import os
import argparse


# In[57]:


def find_ind(grid1d, coord):
        a=abs(grid1d-coord)
        return np.where(a==np.min(a))[0][0]


# In[59]:


def main(input_file, outdir, lat_min,lat_max,lon_min,lon_max):
    ds = xr.open_dataset(input_file,decode_times=False)
    print(f"Opening: {input_file}")
    
    #subset 1: using mask
    subset_ds = ds.where( (ds.nav_lat >= lat_min) & (ds.nav_lat <= lat_max) 
                    & (ds.nav_lon >= lon_min) & (ds.nav_lon <= lon_max), drop=True)
    
    #subset 2: using .isel and indices
    i1 = find_ind(lat_min,ds['nav_lat'][:,0])
    i2 = find_ind(lat_max,ds['nav_lat'][:,0])

    j1 = find_ind(lon_min,ds['nav_lon'][0,:])
    j2 = find_ind(lon_max,ds['nav_lon'][0,:])

    subset_ds2 = ds.isel(y=slice(i1,i2+1),x=slice(j1,j2+1))

    #prepare ouput path and filenames
    input_name = os.path.basename(input_file)
    root_name, ext = os.path.splitext(input_name)
    out_file = os.path.join(outdir, f"{input_name}_subset.nc")
    out_file2 = os.path.join(outdir, f"{input_name}_subset2.nc")
    
    #write subset to file
    subset_ds.to_netcdf(out_file)
    print(f"Subset writted to: {out_file}")
    subset_ds2.to_netcdf(out_file2)
    print(f"Subset2 writted to: {out_file2}")
    

                 


# In[60]:


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Subset NetCDF file by lat/lon bounds")
    parser.add_argument("input_file", help="Path to input NetCDF file")
    parser.add_argument("outdir", help="Output directory")
    parser.add_argument("lat_min", type=float, help="Minimum latitude")
    parser.add_argument("lat_max", type=float, help="Maximum latitude")
    parser.add_argument("lon_min", type=float, help="Minimum longitude")
    parser.add_argument("lon_max", type=float, help="Maximum longitude")

    args = parser.parse_args()

    main(args.input_file, args.outdir, args.lat_min, args.lat_max, args.lon_min, args.lon_max)
    


# In[ ]:




