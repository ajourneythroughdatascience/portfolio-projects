"""
Created on Thu Mar  2 19:30:38 2023

@author: Pablo Aguirre

GitHub: https://github.com/pabloagn
Website: https://pabloagn.com
Contact: https://pabloagn.com/contact

Part of Portfolio Project: sentiment-analysis-in-python
"""

# Third-party packages
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

def happyTransformerModel():
    '''
    Select pretrained model (weights) as source model for transfer learning.
    Define Sentiment Analyzer object.
    Return tokenizer & model objects.
    '''

    model_type = f'cardiffnlp/twitter-roberta-base-sentiment'
    tokenizer = AutoTokenizer.from_pretrained(model_type)
    model = AutoModelForSequenceClassification.from_pretrained(model_type)

    return tokenizer, model