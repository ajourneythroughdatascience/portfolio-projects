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
# Models to Use
# -------------------------------------------------- 
# VADER (Valence Aware Dictionary and sEntiment Reasoner)
# RoBERTa
# TextBlob
# Happy Transformer

# --------------------------------------------------
# Import Modules
# --------------------------------------------------

# Internal modules
# --------------------------------------------------
from .get_parameters import getParameters
from .preprocess_data import preprocessData

# Data manipulation
# --------------------------------------------------
import polars as pl
import numpy as np
import pandas as pd
import pyarrow

# NLP
# --------------------------------------------------
import nltk

# Sentiment Analysis Models
# --------------------------------------------------
# VADER
from nltk.sentiment import SentimentIntensityAnalyzer

# RoBERTa - Hugging Face
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
# We import softmax layers because RoBERTa does not have softmax applied
from scipy.special import softmax

# System
# --------------------------------------------------
import os
import warnings

def runSentimentModel(dataset):

    def vaderAnalyzer():
        
        # We need to download the VADER lexicon first.
        nltk.download('vader_lexicon')
        
        # Define Sentiment Analyzer object
        model = SentimentIntensityAnalyzer()
        
        return model

    def robertaAnalyzer():
        
        # Select pretrained model (weights) as source model for transfer learning.
        model_type = f'cardiffnlp/twitter-roberta-base-sentiment'
        tokenizer = AutoTokenizer.from_pretrained(model_type)

        # Define Sentiment Analyzer object
        model = AutoModelForSequenceClassification.from_pretrained(model_type)

        return tokenizer, model
    
    def applyModel(dataset):
        
        print(f'APPLYING MODEL TO {dataset}')

        # Run Sentiment Analysis
        df = preprocessData(dataset)
        target_col = getParameters()['text_col']
        id_col = getParameters()['target_id_col']
        target_data = df.select([id_col, target_col])

        # Select model
        if getParameters()['model'] == 'VAD':
            model = vaderAnalyzer()

            # Define a dictionary to store resutls
            res_dict = {}

            counter = 0
            total_items = len(df)

            for id, target in target_data.iterrows():
                results = model.polarity_scores(target)

                # Add results to dictionary
                res_dict[id] = results

                # Increment counter
                counter += 1

                print(f'ENTRY {counter} OF {total_items}')

                df_res = (pl.from_pandas((pd.DataFrame(res_dict).T).
                                         reset_index().
                                         rename(columns={'index':'review_id',
                                                         'neg':'VAD_neg',
                                                         'neu':'VAD_neu',
                                                         'pos':'VAD_pos',
                                                         'compound':'VAD_cmp'}
                                                         )
                                        )
                         )

                # Cast new dataframe types
                df_res = df_res.with_column(pl.col('review_id').cast(pl.Categorical))

                # Join with original DataFrame
                df_main = df.join(df_res, on = 'review_id', how="inner")

        elif getParameters()['model'] == 'ROB':
            tokenizer, model = robertaAnalyzer()

            # Define a dictionary to store resutls
            res_dict = {}

            counter = 0
            total_items = len(df)

            for id, target in target_data.iterrows():
                # Encode text
                encoded_target = tokenizer(target, return_tensors='pt')

                # Get scores as tensors
                scores = model(**encoded_target)

                # Convert tensors to numpy array
                results = scores[0][0].detach().numpy()

                # Apply softmax layer (we get array of 3 values per entri: neg, neut, pos)
                results = softmax(results)

                # Populate dictionary with results
                scores_dict = {
                    'ROB_neg' : results[0],
                    'ROB_neu' : results[1],
                    'ROB_pos' : results[2]
                }

                # Add results to dictionary
                res_dict[id] = scores_dict

                # Increment counter
                counter += 1

                print(f'ENTRY {counter} OF {total_items}')

                df_res = pl.from_pandas((pd.DataFrame(res_dict).T).reset_index().rename(columns={'index':'review_id'}))

                # Cast new dataframe types
                df_res = df_res.with_column(pl.col('review_id').cast(pl.Categorical))

                # Join with original DataFrame
                df_main = df.join(df_res, on = 'review_id', how="inner")

        return df_main
    
    df = applyModel(dataset)
    
    return df

# Call main function
if __name__ == '__main__':
    runSentimentModel()