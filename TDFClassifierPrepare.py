#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 22:10:36 2018
Modified from 
https://github.com/t-davidson/hate-speech-and-offensive-language
"""

import pandas as pd
import numpy as np
import pickle
import re

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import classification_report
from sklearn.svm import LinearSVC

def tokenize(tweet):
    """Removes punctuation & excess whitespace, sets to lowercase,
    and stems tweets. Returns a list of stemmed tokens."""
    stemmer = SnowballStemmer("english")
    tweet = " ".join(re.split("[^a-zA-Z]+", tweet.lower())).strip()
    tokens = [stemmer.stem(t) for t in tweet.split()]
    return tokens

def preprocess(text_string):
    """
    Accepts a text string and replaces:
    1) urls with URLHERE
    2) lots of whitespace with one instance
    3) mentions with MENTIONHERE

    This allows us to get standardized counts of urls and mentions
    Without caring about specific people mentioned
    """
    space_pattern = '\s+'
    giant_url_regex = ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
        '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    mention_regex = '@[\w\-]+'
    parsed_text = re.sub(space_pattern, ' ', text_string)
    parsed_text = re.sub(giant_url_regex, '', parsed_text)
    parsed_text = re.sub(mention_regex, '', parsed_text)
    #parsed_text = parsed_text.code("utf-8", errors='ignore')
    return parsed_text

def make_model():
    stopwords = nltk.corpus.stopwords.words("english")
    
    vectorizer = TfidfVectorizer(
        tokenizer=tokenize,
        preprocessor=preprocess,
        ngram_range=(1, 3),
        stop_words=stopwords, #We do better when we keep stopwords
        use_idf=True,
        smooth_idf=False,
        norm=None, #Applies l2 norm smoothing
        decode_error='replace',
        max_features=10000,
        min_df=5,
        max_df=0.501
    )
    
    # load
    df = pd.read_csv("./ref/labeled_data.csv")
    df.columns = df.columns.str.strip()
    tweets = df.tweet
    
    #get feature array
    tfidf = vectorizer.fit_transform(tweets).toarray()
    vocab = {v:i for i, v in enumerate(vectorizer.get_feature_names())}
    print(vocab)
    
    X = pd.DataFrame(tfidf)
    y = df['class'].astype(int)
    
    
    # Get rid of zero values
    # http://scikit-learn.org/stable/modules/feature_selection.html
    select = SelectFromModel(LogisticRegression(class_weight='balanced',penalty="l1",C=0.01))
    X_ = select.fit_transform(X,y)
    
    model = LinearSVC(class_weight='balanced',C=0.01, penalty='l2', \
                      loss='squared_hinge',multi_class='ovr').fit(X_, y)
    y_preds = model.predict(X_)
    report = classification_report( y, y_preds )
    print(report)
    
    with open('SimpleTfidfVectorizer.pkl', 'wb') as fin:
        pickle.dump(vectorizer, fin)
    with open('Selector.pkl', 'wb') as fin:
        pickle.dump(select, fin)
    with open('SVMModel.pkl', 'wb') as fin:
        pickle.dump(model, fin)    


if __name__ == "__main__":
   make_model() 
