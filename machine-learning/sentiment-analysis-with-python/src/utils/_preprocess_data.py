# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 19:23:10 2023

@author: Pablo Aguirre

GitHub: https://github.com/pabloagn
Website: https://pabloagn.com
Contact: https://pabloagn.com/contact

Part of Portfolio Project: sentiment-analysis-in-python
"""

# Third-party packages
import gzip
import polars as pl

# Built-in packages
import os
import time
import urllib.request
import warnings
warnings.filterwarnings('ignore')

# Internal packages
from ._string_formatting import StringFormatting

# Module Settings
pl.toggle_string_cache(True)

class PreprocessData(StringFormatting):
    '''
    '''

    # Import Data
    def downloadMode(self):
        '''
        Enter download mode where all URLs specified on source.txt
        will be downloaded in datasets folder.
        '''
        def downloadData():
            '''
            Download dataset if it does not yet exist.
            '''
            # Define the input file for downloading files using URLs
            input_file = os.path.join(self.project_path, self.var_rdir.get(), self.var_sourceurl.get()) # type: ignore
            counter = 1
            
            # Try to get the source file.
            try:
                file = open(input_file)
                file.close()

            # If it does not exist, return error and notify user
            except Exception as ex:
                self.insertLog(f'ERROR: "{input_file}" DOES NOT EXIST\n\n')
                
                # We will need to manage this return value in the functions refering to it.
                return ex

            with open(input_file, 'r') as url_file:
                len_urls = len(url_file.readlines())

                textvar_downloading = self.padStr('DOWNLOADING FROM:', self.var_sourceurl.get()) # type: ignore
                textvar_linenum = self.padStr('TOTAL URLS:', len_urls)
                
                # Wait for user to see log
                time.sleep(float(self.var_wait_time.get())) # type: ignore

                self.insertLog(f"{textvar_downloading}\n",
                               f"{textvar_linenum}\n")
                    
            with open(input_file, 'r') as url_file:
                progress_1_step = 1/len_urls
                progress_1_perc = 0
                self.progressbar_1.start() # type: ignore
                for url in url_file:
                    # Split on the rightmost / and take everything on the right side of that
                    name = url.split('/')[-1].strip('\n')
                    filename = os.path.join(self.project_path, self.var_rdir.get(), name) # type: ignore
                    
                    if os.path.isfile(filename):
                        self.insertLog(f"ALREADY DOWNLOADED:\n{filename}\n\n")

                    if not os.path.isfile(filename):
                        self.insertLog(f"DOWNLOADING {counter}/{len_urls}:\n{filename}\n\n")
                        urllib.request.urlretrieve(url, filename)
                        self.insertLog(f"DOWNLOADED {counter}/{len_urls}:\n{filename}\n\n")
                        
                    progress_1_perc += progress_1_step
                    self.progressbar_1.set(progress_1_perc) # type: ignore
                    self.update_idletasks() # type: ignore

                    counter += 1

            self.progressbar_1.stop() # type: ignore

            return None
        
        downloadData()

        return None

    def readMode(self, dataset):
        '''
        Enter read mode where a dataset will be read
        if it exists on datasets directory.
        '''

        def selectCols():
            '''
            Get columns required by user.
            '''
            # Build the column aggregation list.
            cols_agg_raw = [self.col_entry_1.get(), # type: ignore
                            self.col_entry_2.get(), # type: ignore
                            self.col_entry_3.get(), # type: ignore
                            self.col_entry_4.get()] # type: ignore
            
            cols_agg = []

            # If user did not specify a given column, do not append it.
            for col in cols_agg_raw:
                if col != '':
                    cols_agg.append(col)

            # Extend list with all other columns
            # We will use this to test if any of the columns does not exist in dataframe
            cols_all = cols_agg.copy()
            cols_all.extend([self.col_rating.get(), # type: ignore
                             self.col_target.get(), # type: ignore
                             self.col_id.get()]) # type: ignore

            cols_text = cols_agg.copy()
            cols_text.extend([self.col_target.get(), self.col_id.get()]) # type: ignore
            
            return cols_all, cols_text, self.col_rating.get(), self.col_target.get() # type: ignore

        def castTypes(df, cols_text, col_rating):
            '''
            Cast columns to appropriate data types for model deployment.
            '''
            # Cast string types
            for text_col in cols_text:
                try:
                    df = df.with_column(pl.col(text_col).cast(pl.Categorical))
                except:
                    try:
                        df = df.with_column(pl.col(text_col).cast(pl.Float64))
                    except:
                        self.insertLog(f'ERROR: COULD NOT CAST {text_col}.\nPLEASE REVIEW DATA ENTRIES\n\n')

            # Cast numerical types
            try:
                df = df.with_column(pl.col(col_rating).cast(pl.Float64))
            
            except:
                self.insertLog(f'ERROR: COULD NOT CAST {col_rating}.\nPLEASE REVIEW DATA ENTRIES\n\n')

            return df

        def readData(dataset):
            '''
            This function will read one file per iteration and return a dataframe.
            It will perform the following tasks:
                - Read file if it exists and is of correct file format.
                - Select user-defined columns if they exist.
                - Cast user-defined columns to correct data type.
                - Return a processed Polars DataFrame object.
            A data set can be in the form of:
                - A compressed .gz file.
                - A .tsv file.
                - A .csv file.
            If dataset does not comply with file format, exception will be raised.
            For collumn selection:
                - A maximum of 4 aggregation columns are allowed.
                - ID column can be of type str or int.
                - Target column requires str type.
                - Rating column can be of type int or float.
            '''

            # Define target path for a given iteration
            read_target = os.path.join(self.project_path, self.var_rdir.get(), dataset) # type: ignore

            # If a .csv file exists, read the .csv file
            if read_target.endswith('.csv'):
                self.insertLog(f"READING:\n{read_target}\n\n")
                termination = '.csv'

                # Wait for user to see params
                time.sleep(float(self.var_wait_time.get())) # type: ignore

                # Read file into df
                df = pl.read_csv(read_target, sep = ',', ignore_errors=True)

                self.insertLog(f"CONCLUDED READING:\n{read_target}\n\n")
                
                # Wait for user to see params
                time.sleep(float(self.var_wait_time.get())) # type: ignore

            # If a .tsv file exists, read the .tsv file
            elif read_target.endswith('.tsv'):
                self.insertLog(f"READING:\n{read_target}\n\n")
                termination = '.tsv'

                # Wait for user to see params
                time.sleep(float(self.var_wait_time.get())) # type: ignore

                # Read file into df
                df = pl.read_csv(read_target, sep = '\t', ignore_errors=True)

                self.insertLog(f"CONCLUDED READING:\n{read_target}\n\n")
            
                # Wait for user to see params
                time.sleep(float(self.var_wait_time.get())) # type: ignore

            # If a .gz file exists, read the .gz file without explicitly decompressing
            elif read_target.endswith('.tsv.gz'):
                self.insertLog(f"READING:\n{read_target}\n\n")
                termination = '.tsv.gz'

                # Wait for user to see params
                time.sleep(float(self.var_wait_time.get())) # type: ignore

                # Read file into df
                with gzip.open(read_target) as compressed_file:
                    df = pl.read_csv(compressed_file.read(), sep = '\t', ignore_errors=True)

                self.insertLog(f"CONCLUDED READING:\n{read_target}\n\n")

                # Wait for user to see params
                time.sleep(float(self.var_wait_time.get())) # type: ignore

            else:
                self.insertLog(f"ERROR:\n{read_target} IS NOT A VALID FILE\n\n")

                # Return error (PENDING)
                return None

            textvar_colnum = self.padStr('COLUMN NUMBER:', len(df.columns))
            self.insertLog(f"{textvar_colnum}\n\n",
                           f"CHECKING COLUMNS\n\n")

            # Wait for user to see params
            time.sleep(float(self.var_wait_time.get())) # type: ignore

            # Extract column list
            cols_all, cols_text, col_rating, col_target = selectCols()

            # Check if user-defined columns exist
            for col in cols_all:
                try:
                    df.select(col)
                # If it does not exist, return error and notify user
                except Exception as ex:
                    self.insertLog(f'ERROR: "{col}" DOES NOT EXIST\n\n')
                
                    # We will need to manage this return value in the functions refering to it.
                    return ex

            df = df.select(cols_all)
            df = castTypes(df, cols_text, col_rating)
            df = df.drop_nulls()

            return df, termination
        
        df, termination = readData(dataset) # type: ignore

        return df, termination

# Call main function
if __name__ == '__main__':
    main() # type: ignore