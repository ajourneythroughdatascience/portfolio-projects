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
from .get_parameters import getParameters

# Data manipulation
# --------------------------------------------------
import polars as pl
import numpy as np

# System
# --------------------------------------------------
import os
import gzip
import shutil
import urllib.request
import re
import warnings

# Module Settings
# --------------------------------------------------
warnings.filterwarnings('ignore')
pl.toggle_string_cache(True)

# --------------------------------------------------
# Import Data
# --------------------------------------------------

def preprocessData(dataset, **kwargs):
    
    def downloadData():

        # A text file (.txt) with all target URLs must be provided
        # If target text files exist, they will not be downloaded. Otherwise, they will be downloaded.
        input_file = os.path.join(getParameters()['inputdir'], getParameters()['source_url'])
        download_dir = getParameters()['rdir']
        counter = 1
        
        with open(input_file, 'r') as url_file:
            x = len(url_file.readlines())
            print(f"DOWNLOADING DATA FROM: {getParameters()['source_url']}")
            print('TOTAL URLS:', x, '\n')
                  
        with open(input_file, 'r') as url_file:
            for url in url_file:
                # Split on the rightmost / and take everything on the right side of that
                name = url.split('/')[-1].strip('\n')
                filename = os.path.join(download_dir, name)
                
                if os.path.isfile(filename):
                    print(f'ALREADY DOWNLOADED: {filename}')
                
                if not os.path.isfile(filename):
                      print(f'DOWNLOADING {counter}/{x}: ' + filename)
                      urllib.request.urlretrieve(url, filename)
                
                counter += 1
        
        return None
    
    def selectCols(df):

        # Get columns from parameters
        target_id_col = getParameters()['target_id_col']
        agg_cols = getParameters()['agg_cols']
        rating_col = getParameters()['rating_col']
        target_col = getParameters()['text_col']

        col_list = agg_cols.copy()
        col_list.extend([rating_col, target_col, target_id_col])

        text_cols = agg_cols.copy()
        text_cols.extend([target_col, target_id_col])

        # Extract the required columns
        try:
            df = df.select(col_list)
        except:
            print('SPECIFIED COLUMNS WERE NOT FOUND ON THE DATA SET.')
            return df
        
        return df, text_cols, rating_col

    def castTypes(df, text_cols, numeric_cols):

        # Cast string types
        for text_col in text_cols:
            try:
                df = df.with_column(pl.col(text_col).cast(pl.Categorical))
            
            except:
                print(f'THERE WAS A DATA TYPE CASTING ERROR WITH {text_col}. PLEASE REVIEW YOUR DATA ENTRIES')

        # Cast numerical types
        try:
            df = df.with_column(pl.col(numeric_cols).cast(pl.Float64))
        
        except:
            print(f'THERE WAS A DATA TYPE CASTING ERROR WITH {numeric_cols}. PLEASE REVIEW YOUR DATA ENTRIES')

        return df

    def normalizeData(dataset):
        # A dataset will be the full path of what the user selects as target
        # We need to load it one by one since sets are too large

        if getParameters()['input_method'] == 'D':
            print('DOWNLOAD MODE', '\n')
            downloadData()
        elif getParameters()['input_method'] == 'R':
            print('READING MODE', '\n')
            print(f'READING {dataset} FROM {getParameters()["rdir"]}')
        
        # A complete data set can be in the form of a .gz file, or a .tsv file.
        # If a .tsv file exists, the .gz file will not get decompressed.
        read_dir = os.path.join(getParameters()['rdir'], dataset)
        if read_dir.endswith('.tsv'):
            print('.TSV FILE EXISTS. READING .TSV FILE')
            df = pl.read_csv(read_dir, sep = '\t', ignore_errors=True)
            
        elif os.path.join(getParameters()['rdir'], dataset).endswith('.tsv.gz'):
            print(f"READING COMPRESSED FILE {dataset}")
            with gzip.open(os.path.join(getParameters()['rdir'], dataset)) as compressed_file:
                df = pl.read_csv(compressed_file.read(), sep = '\t', ignore_errors=True)
        
        print(f"DATASET {dataset} HAS {len(df.columns)} COLUMNS")
        print("TRANSFORMING COLUMNS")

        # Select columns
        df, text_cols, numeric_cols = selectCols(df)

        # Cast data types
        df = castTypes(df, text_cols, numeric_cols)

        # Drop null values
        df = df.drop_nulls()

        return df
    
    df = normalizeData(dataset)

    return df

# Call main function
if __name__ == '__main__':
    preprocessData()