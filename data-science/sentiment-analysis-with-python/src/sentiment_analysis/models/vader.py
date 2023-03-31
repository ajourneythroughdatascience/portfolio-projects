"""
Created on Thu Mar  2 19:30:38 2023

@author: Pablo Aguirre

GitHub: https://github.com/pabloagn
Website: https://pabloagn.com
Contact: https://pabloagn.com/contact

Part of Portfolio Project: sentiment-analysis-in-python
"""

# Third-party packages
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def vaderModel():
    '''
    Download the VADER lexicon first.
    Define Sentiment Analyzer object.
    Return model object.
    '''

    nltk.download('vader_lexicon')
    model = SentimentIntensityAnalyzer()
    
    return model

if __name__ == '__main__':
    vaderModel()