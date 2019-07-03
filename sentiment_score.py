import numpy as np
import pandas as pd
from textblob import TextBlob


def sentiment_score(filename = 'IL.csv'):
    
    raw_data = pd.read_csv(filename, low_memory = True)
    raw_text = []
    text_pol = []
    text_sub = []
    for i in range(len(raw_data['text'])):
        raw_text.append(raw_data['text'][i])

    #to handle the error when the scripts' cods is not in utf-8 format
    for k in range(len(raw_text)):
        raw_text[k] = raw_text[k].decode('utf-8','ignore')

    for j in range(len(raw_data['text'])):
        text_pol.append(TextBlob(raw_text[j]).sentiment.polarity)
        text_sub.append(TextBlob(raw_text[j]).sentiment.subjectivity)

    #dataframe = pd.DataFrame({'polarity':text_pol,'subjectivity':text_sub})
    raw_data = raw_data.drop(['text','Unnamed: 0','Unnamed: 0.1'], axis = 1)
    raw_data['polarity'] = pd.Series(data = text_pol)
    raw_data['subjectivity'] = pd.Series(data = text_sub)
    raw_data.to_csv("IL_new.csv", index = False, sep = ',')
        
sentiment_score()
