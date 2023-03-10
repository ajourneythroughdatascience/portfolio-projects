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
    
    f = open('resources/parameters.json', 'r')
    
    source = json.loads(f.read())

    param_dict = dict(
        input_method = source['input_method'],
        rdir = source['rdir'],
        inputdir = source['inputdir'],
        source_url = source['source_url'],
        target_id_col = source['target_id_col'],
        agg_cols = source['agg_cols'],
        rating_col = source['rating_col'],
        text_col = source['text_col'],
        model = source['model'],
        dataset = source['dataset']
        )
    
    f.close()
    
    return param_dict

# Call main function
if __name__ == '__main__':
    getParameters()