"""
Created on Thu Mar  2 18:25:58 2023

@author: Pablo Aguirre

GitHub: https://github.com/pabloagn
Website: https://pabloagn.com
Contact: https://pabloagn.com/contact

Part of Portfolio Project: sentiment-analysis-in-python
"""

# Third-party packages
import matplotlib
import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import polars as pl
import pyarrow
import seaborn as sns
import xlsxwriter

# Built-in packages
import os
import warnings
warnings.filterwarnings('ignore')

# Define ResultsWriter class
class ResultsWriter:
    '''
    Mixin class:
        - Decide which analysis to write for a given iteration.
        - Get analysis for each iteration.
        - Output files depending on selected analysis.
    '''
    def createDirs(self, result_dict):
        '''
        Create directories for all datasets,
        where we will store all iteration-wise results.
        '''
        for dataset_name, dataset in result_dict.items():

            if not os.path.exists(os.path.join(self.project_path, self.var_wdir.get(), dataset_name)): # type: ignore
                os.makedirs(os.path.join(self.project_path, self.var_wdir.get(), dataset_name)) # type: ignore

        return None
    
    # def preprocessResults(self, df_main, dataset):
    #     '''
    #     Convert polars dataframe to pandas dataframe
    #     '''
    #     self.df = self.df.to_pandas()
    #     print(self.df.head())

    #     return self.df

    def getAttributesParams(self):
        '''
        Extract attributes (Will be the same for all datasets)
        '''
        attributes_params = {'MODEL':self.var_model.get(), # type: ignore
                             'TARGET_COLUMN_ID':self.var_target_id_col.get(), # type: ignore
                             'COLUMN_1':self.var_col1.get(), # type: ignore
                             'COLUMN_2':self.var_col2.get(), # type: ignore
                             'COLUMN_3':self.var_col3.get(), # type: ignore
                             'COLUMN_4':self.var_col4.get(), # type: ignore
                             'RATING_COLUMN':self.var_rating_col.get(), # type: ignore
                             'TARGET_COLUMN':self.var_target_col.get() # type: ignore
                            }

        attributes_params = pd.Series(attributes_params)

        return attributes_params

    def plotTechnical(self, result_dict, res_index):
        '''
        Write the previously generated technical plots.
        '''
        self.insertLog(f'WRITING TECHNICAL PLOTS\n\n') # type: ignore

        for dataset_name, dataset in result_dict.items():
            counter = 0
            for plot in dataset[res_index]:
                filename = os.path.join(self.project_path, self.var_wdir.get(), dataset_name, f'TECHNICAL_{counter}.png') # type: ignore
                plot.savefig(filename,
                             format = 'png',
                             dpi = 300,
                             transparent = self.var_chart_transparency.get() == 'Transparent' # type: ignore
                             )

                counter += 1

        return None

    def plotBusiness(self, result_dict, res_index):
        '''
        Write the previously generated business plots.
        '''
        self.insertLog(f'WRITING BUSINESS PLOTS\n\n') # type: ignore

        for dataset_name, dataset in result_dict.items():
            counter = 0
            for plot in dataset[res_index]:
                filename = os.path.join(self.project_path, self.var_wdir.get(), dataset_name, f'BUSINESS_{counter}.png') # type: ignore
                plot.savefig(filename,
                             format = 'png',
                             dpi = 300,
                             transparent = self.var_chart_transparency.get() == 'Transparent' # type: ignore
                             )

                counter += 1

        return None

    def writeStats(self, result_dict, res_index):
        '''
        Write stats applicable for Technical, Business and Complete.
        '''
        self.insertLog(f'WRITING STATISTICS\n\n') # type: ignore

        for dataset, data in result_dict.items():

            # Write to Excel
            filename = os.path.join(self.project_path, self.var_wdir.get(), dataset, 'STATS.xlsx') # type: ignore

            with pd.ExcelWriter(filename, engine='xlsxwriter') as stats_writer:
                for key, stat in data[res_index].items():
                    stat[0].to_excel(stats_writer, sheet_name=f'{key}_CMP', index=False)
                    stat[1].to_excel(stats_writer, sheet_name=f'{key}_RAT', index=False)

        return None

    def writeTechnical(self, result_dict, res_index):
        '''
        - Write an excel file with tabs:
            - PARAMETERS:
                - model
                - target_id_col,
                - agg_cols,
                - rating_col,
                - target_col.
            - RESULTS:
                - Total entries
                - CMP Median
                - CMP Mean
                - CMP STD
                - CMP MIN
                - CMP Q1
                - CMP Q2
                - CMP Q3
                - CMP MAX
                - SCORE Positive Perc
                - SCORE Neutral Perc
                - SCORE Negative Perc
                - Spearman Rank Corr Coef
                - Spearman Rank Corr P-Value
                - Pearson Corr Coef
                - Pearson Corr P-Value
        '''
        self.insertLog(f'WRITING TECHNICAL REPORT\n\n') # type: ignore

        # Concentrate all technical results in one DataFrame
        df_list = []
        for dataset in result_dict.values():
            df = pd.DataFrame([dataset[res_index]])
            df_list.append(df)
        
        df_technical_full = pd.concat(df_list)

        # Get general parameters and convert to DataFrame
        attributes_params = pd.DataFrame(self.getAttributesParams())

        # Write to Excel
        # Set an Excel file for results writing
        filename = os.path.join(self.project_path, self.var_wdir.get(), 'TECHNICAL.xlsx') # type: ignore

        with pd.ExcelWriter(filename, engine='xlsxwriter') as technical_writer:
            attributes_params.to_excel(technical_writer, sheet_name='PARAMETERS')
            df_technical_full.to_excel(technical_writer, sheet_name='RESULTS', index=False)

        return None

    def writeBusiness(self, result_dict, res_index):
        '''
        - Write an excel file with tabs:
            - PARAMETERS:
                - model
                - target_id_col,
                - agg_cols,
                - rating_col,
                - target_col.
            - RESULTS:
                - Total entries
                - SCORE Positive Perc
                - SCORE Neutral Perc
                - SCORE Negative Perc
        '''
        self.insertLog(f'WRITING BUSINESS REPORT\n\n') # type: ignore

        # Concentrate all technical results in one DataFrame
        df_list = []
        for dataset in result_dict.values():
            df = pd.DataFrame([dataset[res_index]])
            df_list.append(df)
        
        df_business_full = pd.concat(df_list)

        # Get general parameters and convert to DataFrame
        attributes_params = pd.DataFrame(self.getAttributesParams())

        # Write to Excel
        # Set an Excel file for results writing
        filename = os.path.join(self.project_path, self.var_wdir.get(), 'BUSINESS.xlsx') # type: ignore

        with pd.ExcelWriter(filename, engine='xlsxwriter') as technical_writer:
            attributes_params.to_excel(technical_writer, sheet_name='PARAMETERS')
            df_business_full.to_excel(technical_writer, sheet_name='RESULTS', index=False)

        return None

    def writeResults(self, result_dict):
        '''
        Create pack of analyses based on user input.
        '''
        # Create directories
        self.createDirs(result_dict)

        # Option 1: Technical
        # Contains: writeStats, writeTechnical, plotTechnical
        if self.var_analysis.get() == 'Technical': # type: ignore
            self.writeStats(result_dict, 0)
            self.writeTechnical(result_dict, 1)
            self.plotTechnical(result_dict, 2)

        # Option 2: Business
        # Contains: writeStats, writeBusiness, plotBusiness
        elif self.var_analysis.get() == 'Business': # type: ignore
            self.writeStats(result_dict, 0)
            self.writeBusiness(result_dict, 1)
            self.plotBusiness(result_dict, 2)

        # Option 3: Visual
        # Contains: plotTechnical, plotBusiness
        elif self.var_analysis.get() == 'Visual': # type: ignore
            self.plotTechnical(result_dict, 0)
            self.plotBusiness(result_dict, 1)

        # Option 4: Complete
        # Contains: writeStats, writeTechnical, writeBusiness, plotTechnical, plotBusiness
        elif self.var_analysis.get() == 'Complete': # type: ignore
            self.writeStats(result_dict, 0)
            self.writeTechnical(result_dict, 1)
            self.writeBusiness(result_dict, 2)
            self.plotTechnical(result_dict, 3)
            self.plotBusiness(result_dict, 4)
        
        return None

if __name__ == '__main__':
    ResultsWriter()