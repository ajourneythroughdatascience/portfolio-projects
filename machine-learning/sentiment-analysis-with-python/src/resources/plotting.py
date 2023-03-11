# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 19:45:25 2023

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

# Plotting
# --------------------------------------------------
import matplotlib.pyplot as plt
import seaborn as sns

# System
# --------------------------------------------------
import os
import warnings

# --------------------------------------------------
# Define Parameters
# --------------------------------------------------

# Plotting
# --------------------------------------------------

# Before anything else, delete the Matplotlib
# font cache directory if it exists, to ensure
# custom font propper loading
try:
    shutil.rmtree(matplotlib.get_cachedir())
except FileNotFoundError:
    pass

# Define R ggplot style
plt.style.use('ggplot')

# Define main color as hex
color_main = '#1a1a1a'

# Define title & label padding
text_padding = 18

# Define font sizes
title_font_size = 17
label_font_size = 14

# Define rc params
plt.rcParams['figure.figsize'] = [14.0, 7.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['grid.color'] = 'k'
plt.rcParams['grid.linestyle'] = ':'
plt.rcParams['grid.linewidth'] = 0.5
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Lora']

def plotResults():

    

    return None

# Call main function
if __name__ == '__main__':
    main()