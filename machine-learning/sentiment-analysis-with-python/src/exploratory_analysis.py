# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 19:23:42 2023

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

# --------------------------------------------------
# Exploratory Analysis on Sample
# --------------------------------------------------

# Select columns of interest
# --------------------------------------------------

# Load sample data set
df = pl.read_csv(os.path.join(getParameters()['rdir'], 'sample_us.tsv'), sep = '\t')

# Locate columns of interest
df.columns

# Define columns of interest
cols = ['marketplace',
        'product_title',
        'product_category',
        'star_rating',
        'review_headline',
        'review_body',
        'review_date']

# Select cols
df = df.select(cols)

# EDA
# --------------------------------------------------

df.select('star_rating').describe()