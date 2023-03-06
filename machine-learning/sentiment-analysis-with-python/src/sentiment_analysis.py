# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 18:25:58 2023

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
from preprocess_data import preprocessData

# Data manipulation
# --------------------------------------------------
import polars as pl
import numpy as np

# NLP
# --------------------------------------------------
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# System
# --------------------------------------------------
import os
import warnings

# --------------------------------------------------
# First Approach: VADER (Valence Aware Dictionary and sEntiment Reasoner)
# --------------------------------------------------

def runSentimentModel(**kwargs):

    def vaderAnalyzer():
        
        # We need to download the VADER lexicon first.
        if not os.path.exists('C:/Users/pablo/AppData/Roaming/nltk_data/sentiment'):
            nltk.download('vader_lexicon')
        
        # Define Sentiment Analyzer object
        model = SentimentIntensityAnalyzer()
        
        return model

    def robertaAnalyzer():
        
        df = preprocessData()
        
        # Define Sentiment Analyzer object
        model = SentimentIntensityAnalyzer()
        
        return model
    
    def applyModel():
        
        df = preprocessData()
        
        if getParameters()['model'] == 'VAD':
            model = vaderAnalyzer()
            
            results = df.with_columns([
                pl.col('review_body').map(lambda s: model.polarity_scores(s).alias("activations"))
                ]).collect()
            
        elif getParameters()['model'] == 'ROB':
            model = robertaAnalyzer()
        

        
        return results
    
    df = applyModel()
    
    return df





