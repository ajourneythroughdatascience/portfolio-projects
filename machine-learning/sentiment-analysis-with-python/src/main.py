# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 19:30:38 2023

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
import resources

# System Modules
# --------------------------------------------------
import os
import warnings
warnings.filterwarnings("ignore")

# --------------------------------------------------
# Run Sentiment Analysis algorithm
# --------------------------------------------------

# Define main function

def main():
    print("SENTIMENT ANALYSIS 1.0")
    print("WRITTEN BY PABLO AGUIRRE")
    
    # Define the target dataset
    target_dataset = resources.getParameters()['dataset']
    rdir = resources.getParameters()['rdir']

    for target in target_dataset:
        # Create target path
        dataset = os.path.join(rdir, target)
        # Perform Sentiment Analysis
        df = resources.runSentimentModel(dataset)

    return df

# Call main function
if __name__ == '__main__':
    main()