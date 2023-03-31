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
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import numpy as np
import pandas as pd
import polars as pl
from scipy.stats import spearmanr
from scipy.stats import pearsonr
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# Built-in packages
import os
import shutil
import warnings
warnings.filterwarnings('ignore')

class ResultsAnalysis:
    '''
    Collect iteration information.
    Perform analyses to pass to writing.
    '''

    # Set global parameters
    plt.rcParams['figure.figsize'] = [14.0, 7.0]
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['grid.color'] = 'k'
    plt.rcParams['grid.linestyle'] = ':'
    plt.rcParams['grid.linewidth'] = 0.5
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Lora']
    plt.rcParams["figure.titlesize"] = 18

    def setScoresComp(self, score):
        '''
        Sets sentiment tag based on compound score.
        '''
        if score < 0:
            return "Negative"
        
        elif score == 0:
            return "Neutral"
        
        else:
            return "Positive"

    def getPercentages(self, df_processed):
        '''
        Calculates percentages for Positive, Neutral and Negative
        based on score.
        '''
        total_len = len(df_processed)

        positive_perc = round((len(df_processed[df_processed['SCORE'] == 'Positive']) / total_len), 4)
        neutral_perc = round((len(df_processed[df_processed['SCORE'] == 'Neutral']) / total_len), 4)
        negative_perc = round((len(df_processed[df_processed['SCORE'] == 'Negative']) / total_len), 4)

        return positive_perc, neutral_perc, negative_perc

    def calculateCorrelation(self, df_processed):
        '''
        Calculates the correlation between
        the compound score and the actual rating.
            - Spearman Rank Coefficient
            - Pearson Coefficient
        Calculates the p-value associated
        with this correlation.
            - Spearman Rank Coefficient P-Value
            - Pearson Coefficient P-Value
        Provides the user two measures
        with which to trust/not trust the model results.
        '''
        # First, scale our data for results to be coherent
        df_ratings = df_processed[self.var_rating_col.get()].values # type: ignore
        df_scores = df_processed['CMP'].values

        scaler = MinMaxScaler(feature_range=(0, 1))

        ratings_scaled = scaler.fit_transform([[x] for x in df_ratings])[:,0]
        scores_scaled = scaler.fit_transform([[x] for x in df_scores])[:,0]
        
        # Calculate Pearson Rank & Spearman
        coef_s, p_s = spearmanr(ratings_scaled, scores_scaled)
        coef_p, p_p = pearsonr(ratings_scaled, scores_scaled)

        return coef_s, p_s, coef_p, p_p

    def findTags(self, tag_prefix, tagged_text):
        '''
        Get the most frequent words
        per selected nltk tag using
        the var_top_words param.
        '''
        cfd = nltk.ConditionalFreqDist((tag, word.lower()) for (word, tag) in tagged_text if tag == tag_prefix)

        return dict((tag, cfd[tag].most_common(int(self.var_top_words.get()))) for tag in cfd.conditions()) # type: ignore

    def performGrammaticalAnalysis(self,
                                   df_subset,
                                   nltk_tags,
                                   banned_chars,
                                   grammatical_tags):
        '''
        Perform word frequency analysis per POS.
        '''
        # Perform grammatical frequency analysis
        tag_frequency = {}
        tokenized_pos_all = []

        for i, target in df_subset.iterrows():
    
            # Tokenize string into list of substrings
            tokenized = nltk.word_tokenize(str(target[self.var_target_col.get()])) # type: ignore
            
            # Remove banned chars
            tokenized = [x for x in tokenized if x not in banned_chars]
            
            # Calculate pos
            tokenized_pos = nltk.pos_tag(tokenized)
            tokenized_pos_all.extend(tokenized_pos)

        for nltk_tag in nltk_tags:
            
            # Analyze
            tagdict = self.findTags(nltk_tag, tokenized_pos_all)
            for tag in sorted(tagdict):
                tag_frequency[tag] = tagdict[tag]

        # Unbound big list from memory
        del tokenized_pos_all

        # Convert tags to name descriptions
        tag_frequency = { grammatical_tags.get(k, k): v for k, v in tag_frequency.items() }

        return tag_frequency

    def getGrammaticalDetail(self, df_processed):
        '''
        Get the grammatical frequency
        of top and bottom performing subsets
        '''
        # Define a set of banned characters (will not be included in analysis)
        banned_chars = ['\n', '\t', 'br', '<', '>', '/', '#', ']', '[', '-']

        # Define the NLTK tags of interest
        nltk_tags = ['NN', 'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS']

        # Define NLTK Tag Description
        grammatical_tags = {'NN':'Noun, Common, Singular or Mass',
                            'NNP':'Noun, Proper, Singular',
                            'NNS':'Noun, Common, Plural',
                            'JJ':'Adjective, Ordinal',
                            'JJR':'Adjective, Comparative',
                            'JJS':'Adjective, Superlative',
                            'RB':'Adverb',
                            'RBR':'Adverb, Comparative',
                            'RBS':'Adverb, Superlative'
                            }

        # Perform for top subset using var_nltk_threshold
        tag_frequency_top = self.performGrammaticalAnalysis(df_processed[df_processed['CMP'] >= self.var_nltk_threshold.get()], # type: ignore
                                                            nltk_tags,
                                                            banned_chars,
                                                            grammatical_tags
                                                            )
        
        # Perform for bottom subset using var_nltk_threshold
        tag_frequency_bottom = self.performGrammaticalAnalysis(df_processed[df_processed['CMP'] <= -self.var_nltk_threshold.get()], # type: ignore
                                                               nltk_tags,
                                                               banned_chars,
                                                               grammatical_tags
                                                               )

        return tag_frequency_top, tag_frequency_bottom

    def plotGrammaticalDetail(self,
                              tag_frequency,
                              grammatical,
                              axis,
                              counter):
        '''
        Generate a new figure.
        Plot the word frequency.
        Return a figure containing the plot.
        '''
        df = pd.DataFrame(tag_frequency[grammatical],
                          columns = ['Word', 'Frequency'])

        df.plot(kind='bar',
                x='Word',
                y='Frequency',
                ax = axis[counter],
                cmap = self.var_plot_colorscheme.get()) # type: ignore

        axis[counter].set_title(grammatical)

    def plotWordCloud(self, df_processed):
        '''
        Generate wordcloud figure
        on most repeated words per dataset.
        SOURCE: https://samuelndungula.medium.com/sentiment-analysis-using-vader-and-roberta-5279ba312d70
        '''
        # Define font path
        font_path = os.path.join(self.project_path, 'src', 'digital_assets', 'Cardo-Regular.ttf') # type: ignore

        # Create stopword
        stopwords = set(STOPWORDS)

        words_all = ' '.join([str(words) for words in df_processed[self.var_target_col.get()]]) # type: ignore

        word_cloud = WordCloud(width=3200,
                               height=1600,
                               random_state=10,
                               stopwords=stopwords,
                               background_color='black',
                               colormap=self.var_plot_colorscheme.get(), # type: ignore
                               collocations=False,
                               font_path = font_path
                               ).generate(words_all)
        
        fw, wx = plt.subplots(figsize=(20,10))
        wx.imshow(word_cloud, interpolation='bilinear')
        plt.tight_layout(pad=0)
        plt.axis('off')
        plt.close(fw)

        return fw

    def plotAggCols(self, agg_col, df_agg):
        '''
        For each agg column,
        plot a rating per agg level 100%
        stacked bar chart.
        '''
        f_2_5, ax_2_5 = plt.subplots()

        p_2_5 = df_agg.plot(kind='barh',
                            stacked=True,
                            ax = ax_2_5,
                            cmap = self.var_plot_colorscheme.get()) # type: ignore

        p_2_5.set_title(agg_col) # type: ignore
        plt.close(f_2_5)

        return f_2_5
    
    def plotHeatMap(self, agg_col, df_agg, agg_target):
        '''
        For each agg column,
        plot a rating per agg level 100%
        heatmap.
        '''

        f_6_9, ax_6_9 = plt.subplots()

        pb_6_9 = sns.heatmap(df_agg,
                             ax = ax_6_9,
                             cmap = self.var_plot_colorscheme.get() # type: ignore
                             )

        plt.close(f_6_9)

        f_6_9.suptitle(f'Heatmap For: {agg_col} vs. {agg_target}',
                        y = self.subptitle_y) # type: ignore

        return f_6_9

    def generateTechnicalCalc(self,
                              df_processed,
                              dataset,
                              score_percentages):
        '''
        For each iteration, calculates the following:
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
        # Calculate additional attributes
        cmp_description = df_processed['CMP'].describe()

        # Extract info from statistial description
        cmp_count = cmp_description['count']
        cmp_mean = cmp_description['mean']
        cmp_std = cmp_description['std']
        cmp_min = cmp_description['min']
        cmp_q1 = cmp_description['25%']
        cmp_q2 = cmp_description['50%']
        cmp_q3 = cmp_description['75%']
        cmp_max = cmp_description['max']

        # Get confidence measure
        coef_s = self.calculateCorrelation(df_processed)[0]
        p_s = self.calculateCorrelation(df_processed)[1]

        coef_p = self.calculateCorrelation(df_processed)[2]
        p_p = self.calculateCorrelation(df_processed)[3]

        # Get grammatical detail
        tag_frequency_top, tag_frequency_bottom = self.getGrammaticalDetail(df_processed)

        # Build dictionary
        technical_calc = {'DATASET':dataset.name,
                          'TOTAL_ENTRIES':cmp_count,
                          'MEDIAN':np.median(df_processed['CMP']),
                          'MEAN':cmp_mean,
                          'STANDARD_DEVIATION':cmp_std,
                          'MIN_VALUE':cmp_min,
                          'FIRST_QUARTILE':cmp_q1,
                          'SECOND_QUARTILE':cmp_q2,
                          'THIRD_QUARTILE':cmp_q3,
                          'MAX_VALUE':cmp_max,
                          'POSITIVE_PERCENTAGE':score_percentages[0],
                          'NEUTRAL_PERCENTAGE':score_percentages[1],
                          'NEGATIVE_PERCENTAGE':score_percentages[2],
                          'SPEARMAN_RANK_CORRELATION':coef_s,
                          'SPEARMAN_RANK_P_VALUE':p_s,
                          'PEARSON_CORRELATION':coef_p,
                          'PEARSON_P_VALUE':p_p
                          }

        technical_calc = pd.Series(technical_calc)

        return technical_calc, tag_frequency_top, tag_frequency_bottom

    def generateBusinessCalc(self,
                             df_processed,
                             dataset,
                             score_percentages):
        '''
        For each iteration, calculates the following:
            - Total entries
            - SCORE Positive Perc
            - SCORE Neutral Perc
            - SCORE Negative Perc
        '''
        # First, aggregate

        business_calc = {'DATASET':dataset.name,
                         'TOTAL_ENTRIES':len(df_processed),
                         'POSITIVE_PERC':score_percentages[0],
                         'NEUTRAL_PERC':score_percentages[1],
                         'NEGATIVE_PERC':score_percentages[2]
                        }

        return business_calc

    def generateStats(self, df_processed, agg_col_list):
        '''
        Calculate Mean and Standard Deviation
        of Compound and Rating for all
        aggregation Levels.
        '''
        
        stats_dict = {}

        for col in agg_col_list:
            stats = []
            df_stats_compound = (df_processed.groupby([col], as_index=False).
                                 agg({'CMP':['mean','std']}) # type: ignore
                                 )
            
            df_stats_compound.columns = [col, 'MEAN', 'STD']

            stats.append(df_stats_compound)

            df_stats_rating = (df_processed.groupby([col], as_index=False).
                               agg({self.var_rating_col.get():['mean','std']}) # type: ignore
                               )

            df_stats_rating.columns = [col, 'MEAN', 'STD']

            stats.append(df_stats_rating)
            
            stats_dict[col] = stats

        return stats_dict

    def generateTechnicalPlots(self,
                               tag_frequency_top,
                               tag_frequency_bottom):
        '''
        For each iteration, generate technical plots.
        '''
        # Define counter for subplot index setting
        counter = 0

        # Plot 1: Word frequency for highest rated composition scores per grammatical object
        f1, ax_1 = plt.subplots(3, 3, figsize=(12, 12))

        # Unpack axes
        ax_1 = ax_1.ravel() # type: ignore

        for grammatical in tag_frequency_top:
            self.plotGrammaticalDetail(tag_frequency_top, grammatical, ax_1, counter)
        
            counter += 1

        f1.suptitle('Word Frequency for Highest Ratings',
                    y = self.subptitle_y # type: ignore
                    )
        
        plt.tight_layout()
        plt.close(f1)

        counter = 0

        # Plot 2: Word frequency for lowest rated composition scores per grammatical object
        f2, ax_2 = plt.subplots(3, 3, figsize=(12, 12))

        # Unpack axes
        ax_2 = ax_2.ravel() # type: ignore

        for grammatical in tag_frequency_bottom:
            self.plotGrammaticalDetail(tag_frequency_bottom, grammatical, ax_2, counter)
        
            counter += 1

        f2.suptitle('Word Frequency for Lowest Ratings',
                    y = self.subptitle_y) # type: ignore
        
        plt.tight_layout()
        plt.close(f2)

        return f1, f2

    def generateBusinessPlots(self,
                              df_processed,
                              agg_col_list):
        '''
        For each iteration, plots the following figures:
            - Figure 1: Compound Score vs Rating Barplot (SOURCE: https://www.youtube.com/watch?v=QpzMWQvxXWk&t=1164s).
            - Figure 2_5: Rating per agg level 1_4 100% Stacked Bar Chart.
            - Figure 6_9: Plot pairs for worst and best values in terms of composed sentiment analysis for each agg column
            - Figure 10: Word cloud (all forms of speech).
        '''
        # Plot 1: Compound Score vs Rating Barplot
        fig_list = []
        f1, ax_1 = plt.subplots()
        p_1 = sns.barplot(data = df_processed,
                          x = self.var_rating_col.get(), # type: ignore
                          y = 'CMP',
                          ax = ax_1,
                          palette = self.var_plot_colorscheme.get() # type: ignore
                          )

        p_1.set_title('Compound Score by Ratings')
        plt.close(f1)
        fig_list.append(f1)

        # Call plot generator
        for agg_col in agg_col_list:
            if agg_col != '':
                # Aggregate results
                df_agg_score = (df_processed.groupby([agg_col])['SCORE']. # type: ignore
                                value_counts(normalize=True).
                                unstack(agg_col) # type: ignore
                               ).T # Transpose required: We need agg_col on x and star rating composition on y
                
                df_agg_rating = (df_processed.groupby([agg_col])[self.var_rating_col.get()]. # type: ignore
                                 value_counts(normalize=True).
                                 unstack(agg_col) # type: ignore
                                ).T # Transpose required: We need agg_col on x and star rating composition on y         

                f2_5 = self.plotAggCols(agg_col, df_agg_score)
                fig_list.append(f2_5)

                f6_9 = self.plotHeatMap(agg_col, df_agg_score, 'Score')
                fig_list.append(f6_9)

                f10_13 = self.plotHeatMap(agg_col, df_agg_rating, self.var_rating_col.get()) # type: ignore
                fig_list.append(f10_13)     

        f15 = self.plotWordCloud(df_processed)
        fig_list.append(f15)

        return fig_list

    def performAnalysis(self, df_main, dataset):
        '''
        1. Extract attributes:
            - model, target_id_col, agg_cols, rating_col, target_col, number_of_datasets_analyzed
        2. Convert df_main to Pandas DataFrame
        3. Calculate additional attributes (cmp = COMPOUND, {-1, 1}):
            - dataset, total_entries, cmp_median, cmp_mean, cmp_std, cmp_min, cmp_q1, cmp_q2, cmp_q3, cmp_max.
        4. Return a tuple of Pandas Series containing all analysis for writing.
        '''
        start_analysis_log = self.padStr('PERFORMING ANALYSIS:', self.var_analysis.get()) # type: ignore
        self.insertLog(f'{start_analysis_log}\n\n') # type: ignore

        # Process DataFrame
        df_processed = df_main.to_pandas()

        # Set score based on cmp
        df_processed['SCORE'] = df_processed['CMP'].apply(self.setScoresComp)
        df_processed = df_processed.fillna(0)

        # Calculate percentages
        score_percentages = self.getPercentages(df_processed)

        # Pack agg cols in a list
        agg_col_list = [self.var_col1.get(), # type: ignore
                        self.var_col2.get(), # type: ignore
                        self.var_col3.get(), # type: ignore
                        self.var_col4.get()  # type: ignore
                        ]

        # Option 1: Technical
        # Contains: generateTechnicalCalc, generateTechnicalPlots
        if self.var_analysis.get() == 'Technical': # type: ignore
            progress_3_step = 1/3
            progress_3_perc = 0
            self.progressbar_3.start() # type: ignore

            stats = self.generateStats(df_processed, agg_col_list)
            progress_3_perc += progress_3_step
            self.progressbar_3.set(progress_3_perc) # type: ignore
            self.update_idletasks() # type: ignore

            technical_calc, tag_frequency_top, tag_frequency_bottom = self.generateTechnicalCalc(df_processed, dataset, score_percentages)
            progress_3_perc += progress_3_step
            self.progressbar_3.set(progress_3_perc) # type: ignore
            self.update_idletasks() # type: ignore

            technical_plots = self.generateTechnicalPlots(tag_frequency_top, tag_frequency_bottom)
            progress_3_perc += progress_3_step
            self.progressbar_3.set(progress_3_perc) # type: ignore
            self.update_idletasks() # type: ignore

            self.progressbar_3.stop() # type: ignore

            return (stats,
                    technical_calc,
                    technical_plots
                    )
        
        # Option 2: Business
        # Contains: generateBusinessCalc, generateBusinessPlots, generateWordCloud
        elif self.var_analysis.get() == 'Business': # type: ignore
            progress_3_step = 1/3
            progress_3_perc = 0
            self.progressbar_3.start() # type: ignore

            stats = self.generateStats(df_processed, agg_col_list)
            progress_3_perc += progress_3_step
            self.progressbar_3.set(progress_3_perc) # type: ignore
            self.update_idletasks() # type: ignore

            business_calc = self.generateBusinessCalc(df_processed, dataset, score_percentages)
            progress_3_perc += progress_3_step
            self.progressbar_3.set(progress_3_perc) # type: ignore
            self.update_idletasks() # type: ignore
            
            business_plots = self.generateBusinessPlots(df_processed, agg_col_list)
            progress_3_perc += progress_3_step
            self.progressbar_3.set(progress_3_perc) # type: ignore
            self.update_idletasks() # type: ignore
            
            self.progressbar_3.stop() # type: ignore

            return (stats,
                    business_calc,
                    business_plots
                    )
        
        # Option 3: Visual
        # Contains: generateTechnicalPlots, generateBusinessPlots, generateWordCloud
        elif self.var_analysis.get() == 'Visual': # type: ignore
            progress_3_step = 1/3
            progress_3_perc = 0
            self.progressbar_3.start() # type: ignore

            technical_calc, tag_frequency_top, tag_frequency_bottom = self.generateTechnicalCalc(df_processed, dataset, score_percentages)
            progress_3_perc += progress_3_step
            self.progressbar_3.set(progress_3_perc) # type: ignore
            self.update_idletasks() # type: ignore

            technical_plots = self.generateTechnicalPlots(tag_frequency_top, tag_frequency_bottom)
            progress_3_perc += progress_3_step
            self.progressbar_3.set(progress_3_perc) # type: ignore
            self.update_idletasks() # type: ignore

            business_plots = self.generateBusinessPlots(df_processed, agg_col_list)
            progress_3_perc += progress_3_step
            self.progressbar_3.set(progress_3_perc) # type: ignore
            self.update_idletasks() # type: ignore

            self.progressbar_3.stop() # type: ignore

            return (technical_calc,
                    technical_plots,
                    business_plots
                    )
        
        # Option 4: Complete
        # Contains: generateTechnicalCalc, generateBusinessCalc, generateTechnicalPlots, generateBusinessPlots, generateWordCloud
        elif self.var_analysis.get() == 'Complete': # type: ignore
            progress_3_step = 1/5
            progress_3_perc = 0

            self.progressbar_3.start() # type: ignore

            stats = self.generateStats(df_processed, agg_col_list)
            progress_3_perc += progress_3_step
            self.progressbar_3.set(progress_3_perc) # type: ignore
            self.update_idletasks() # type: ignore

            technical_calc, tag_frequency_top, tag_frequency_bottom = self.generateTechnicalCalc(df_processed, dataset, score_percentages)
            progress_3_perc += progress_3_step
            self.progressbar_3.set(progress_3_perc) # type: ignore
            self.update_idletasks() # type: ignore
            
            business_calc = self.generateBusinessCalc(df_processed, dataset, score_percentages)
            progress_3_perc += progress_3_step
            self.progressbar_3.set(progress_3_perc) # type: ignore
            self.update_idletasks() # type: ignore
            
            technical_plots = self.generateTechnicalPlots(tag_frequency_top, tag_frequency_bottom)
            progress_3_perc += progress_3_step
            self.progressbar_3.set(progress_3_perc) # type: ignore
            self.update_idletasks() # type: ignore
            
            business_plots = self.generateBusinessPlots(df_processed, agg_col_list)
            progress_3_perc += progress_3_step
            self.progressbar_3.set(progress_3_perc) # type: ignore
            self.update_idletasks() # type: ignore
            
            self.progressbar_3.stop() # type: ignore

            return (stats,
                    technical_calc,
                    business_calc,
                    technical_plots,
                    business_plots
                    )
        
if __name__ == '__main__':
    ResultsAnalysis()