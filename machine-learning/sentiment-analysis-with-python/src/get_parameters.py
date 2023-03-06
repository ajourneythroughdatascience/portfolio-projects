# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 19:29:01 2023

@author: pablo

GitHub: https://github.com/pabloagn
Website: https://pabloagn.com
Contact: https://pabloagn.com/contact

Part of Portfolio Project: sentiment-analysis-in-python
"""

# --------------------------------------------------
# Import Modules
# --------------------------------------------------

# Data manipulation
# --------------------------------------------------
import json

# --------------------------------------------------
# Get Parameters from JSON File
# --------------------------------------------------

def getParameters(**kwargs):
    
    f = open('parameters.json', 'r')
    
    source = json.loads(f.read())

    param_dict = dict(
        rdir = source['rdir'],
        sample_file = source['sample_file'],
        complete_file = source['complete_file'],
        source_url = source['source_url'],
        cols = source['cols'],
        model = source['model']
        )
    
    f.close()
    
    return param_dict