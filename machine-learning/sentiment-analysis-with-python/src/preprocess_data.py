# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 19:23:10 2023

@author: pablo

GitHub: https://github.com/pabloagn
Website: https://pabloagn.com
Contact: https://pabloagn.com/contact

Part of Portfolio Project: sentiment-analysis-in-python
"""

# --------------------------------------------------
# Import Modules
# --------------------------------------------------

# Internal modules
# --------------------------------------------------
from get_parameters import getParameters

# Data manipulation
# --------------------------------------------------
import polars as pl
import numpy as np

# System
# --------------------------------------------------
import os
import warnings
import gzip
import shutil
import urllib.request
import re

# --------------------------------------------------
# Import Data
# --------------------------------------------------

def preprocessData(**kwargs):
    
    def downloadData():
        print('Downloading data from AWS')
        # A text file with all Amazon download URLs must be provided.
        # If files exist, they will not be downloaded. Otherwise, they will be downloaded.
        download_dir = getParameters()['rdir']
        counter = 1
        
        with open(getParameters()['source_url'], 'r') as url_file:
            x = len(url_file.readlines())
            print('Total URLs:', x)
            
            for url in url_file:
                
                # Split on the rightmost / and take everything on the right side of that
                name = re.search('amazon_reviews_us_(.*)_v1_00', url).group(1)
                filename = os.path.join(download_dir, name)
                
                if not os.path.isfile(filename):
                      print(f'Downloading {counter}/{x}: ' + filename)
                      urllib.request.urlretrieve(url, filename)
                
                counter += 1
                
        return None
    
    def importData():
        
        preprocessData()
        
        # A complete data set can be in the form of a .gz file, or a .tsv file.
        # If a .tsv file exists, the .gz file will not get decompressed.
        if os.path.exists(os.path.join(getParameters()['rdir'], f"{getParameters()['complete_file']}.tsv")):
            print(f"WARNING: {getParameters()['complete_file']}.tsv already exists.")
            print('Reading .tsv file.')
            
        else:
            print(f"Extracting {getParameters()['complete_file']}.gz to {getParameters()['complete_file']}.tsv")
            with gzip.open(os.path.join(getParameters()['rdir'], f"{getParameters()['complete_file']}.gz"), 'rb') as f_in:
                with open(os.path.join(getParameters()['rdir'], f"{getParameters()['complete_file']}.tsv"), 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        
        # File will be read to a Polars LazyFrame object
        df = pl.scan_csv(os.path.join(getParameters()['rdir'], f"{getParameters()['complete_file']}.tsv"), sep = '\t')
        
        return None

    def transformData():
        
        df = importData()
        
        # We will only select the columns specified in JSON parameters file
        df = df.select(getParameters()['cols'])
        try:
            df = df.select(getParameters()['cols'])
        except:
            print('Some or all of the specified columns were not found on the data set.')
        
        return None
        
    df = downloadData()

    return df