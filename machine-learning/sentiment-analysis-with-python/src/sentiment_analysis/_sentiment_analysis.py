"""
Created on Thu Mar  2 18:25:58 2023

@author: Pablo Aguirre

GitHub: https://github.com/pabloagn
Website: https://pabloagn.com
Contact: https://pabloagn.com/contact

Part of Portfolio Project: sentiment-analysis-in-python
"""

# Third-party packages
import numpy as np
import pandas as pd
import polars as pl
import pyarrow
from textblob import TextBlob

# Built-in packages
import os
import time
import warnings
warnings.filterwarnings('ignore')

# Internal packages
from utils import PreprocessData
from sentiment_analysis.models import vader
from ._results_analysis import ResultsAnalysis
from ._results_writer import ResultsWriter

# Define SentimentAnalysis class
class SentimentAnalysis(PreprocessData,
                        ResultsAnalysis,
                        ResultsWriter):
    '''
    Perform sentiment analysis on a given data set.
    '''

    def applyModel(self, df, dataset):
        '''
        Apply sentiment analysis model depending on user's choice.
        '''
        self.insertLog(f'APPLYING MODEL TO {dataset.name}\n\n')

        time.sleep(float(self.var_wait_time.get())) # type: ignore

        # Run Sentiment Analysis
        target_data = df.select([self.col_id.get(), # type: ignore
                                 self.col_target.get()]) # type: ignore

        # Select model
        if self.var_model.get() == 'VADER': # type: ignore
            model = vader.vaderModel()

            # Define a dictionary to store resutls
            res_dict = {}

            counter = 0

            # Start progress bar
            total_items = len(df)
            progress_2_step = 1/total_items
            progress_2_perc = 0
            self.progressbar_2.start() # type: ignore

            for col_id, target in target_data.iterrows():
                results = model.polarity_scores(target)

                # Add results to dictionary
                res_dict[col_id] = results

                # Increment counter
                counter += 1
                self.insertLog(f'ENTRY {counter} OF {total_items}\n')
                
                # Update progress bar
                progress_2_perc += progress_2_step
                self.progressbar_2.set(progress_2_perc) # type: ignore
                self.update_idletasks() # type: ignore

            # Stop progress bar
            self.progressbar_2.stop() # type: ignore

            df_res = (pl.from_pandas((pd.DataFrame(res_dict).T).
                                        reset_index().
                                        rename(columns={'index':self.col_id.get(), # type: ignore
                                                        'neg':'NEG',
                                                        'neu':'NEU',
                                                        'pos':'POS',
                                                        'compound':'CMP'}
                                                        )
                                    )
                        )

            # Cast new dataframe types
            df_res = df_res.with_column(pl.col(self.col_id.get()).cast(pl.Categorical)) # type: ignore
            
            # We won't be using Positive, Neutral and Negative Scores, only Compound
            df_res = df_res.drop(columns = ['POS', 'NEU', 'NEG'])

            # Join with original DataFrame
            df_main = df.join(df_res, on = self.col_id.get(), how="inner") # type: ignore

        elif self.var_model.get() == 'TextBlob': # type: ignore
            # Define a dictionary to store resutls
            res_dict = {}

            counter = 0

            # Start progress bar
            total_items = len(df)
            progress_2_step = 1/total_items
            progress_2_perc = 0
            self.progressbar_2.start() # type: ignore

            for col_id, target in target_data.iterrows():
                results = TextBlob(str(target))
                polarity_score = results.sentiment.polarity # type: ignore

                # Add results to dictionary
                res_dict[col_id] = {'compound':round(polarity_score, 4)}

                # Increment counter
                counter += 1
                self.insertLog(f'ENTRY {counter} OF {total_items}\n')
                
                # Update progress bar
                progress_2_perc += progress_2_step
                self.progressbar_2.set(progress_2_perc) # type: ignore
                self.update_idletasks() # type: ignore

            # Stop progress bar
            self.progressbar_2.stop() # type: ignore

            df_res = (pl.from_pandas((pd.DataFrame(res_dict).T).
                                        reset_index().
                                        rename(columns={'index':self.col_id.get(), # type: ignore
                                                        'compound':'CMP'}
                                                        )
                                    )
                        )

            # Cast new dataframe types
            df_res = df_res.with_column(pl.col(self.col_id.get()).cast(pl.Categorical)) # type: ignore

            # Join with original DataFrame
            df_main = df.join(df_res, on = self.col_id.get(), how="inner") # type: ignore

        return df_main # type: ignore

    def executeModel(self):
        '''
        Downloads datasets if user has requested Download operations. 
        Loads data sets one by one and perform analysis per dataset.
        '''
        # Enter download mode
        if self.var_operation.get() == 'Download Mode': # type: ignore
            self.insertLog("ENTERING DOWNLOAD MODE\n\n")

            # Wait
            time.sleep(float(self.var_wait_time.get())) # type: ignore

            # Download files
            self.downloadMode()

        # Enter reading mode
        elif self.var_operation.get() == 'Read Mode': # type: ignore
            self.insertLog("ENTERING READ MODE\n\n")

            # Wait 2 seconds (for user to see params)
            time.sleep(float(self.var_wait_time.get())) # type: ignore

        # Count number of files
        file_count = 0
        with os.scandir(os.path.join(self.project_path, self.var_rdir.get())) as datasets: # type: ignore
            for dataset in datasets:
                if dataset.name != self.var_sourceurl.get(): # type: ignore
                    file_count =+ 1

        # Read all files in directory, regardless of mode
        with os.scandir(os.path.join(self.project_path, self.var_rdir.get())) as datasets: # type: ignore

            if file_count == 0:
                self.insertLog("WARNING: FILE NOT FOUND\n\n")
                
                return None

            else:
                result_dict = {}
                for dataset in datasets:
                    # Excluding URL source file
                    if dataset.name != self.var_sourceurl.get(): # type: ignore
                        # Read mode
                        self.progressbar_1.set(0) # type: ignore
                        df, termination = self.readMode(dataset)
                        self.progressbar_1.set(1) # type: ignore
                        self.update_idletasks() # type: ignore
                        self.progressbar_1.stop() # type: ignore
                        # Apply model
                        df_main = self.applyModel(df, dataset)

                        # Remove termination from file
                        dataset_name = dataset.name.replace(termination, '')

                        # Apply analysis on each iteration and save results\
                        result_dict[dataset_name] = self.performAnalysis(df_main, dataset)

        # Perform writing
        self.writeResults(result_dict) # type: ignore

        return None

if __name__ == '__main__':
    main() # type: ignore