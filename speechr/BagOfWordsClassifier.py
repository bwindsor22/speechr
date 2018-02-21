#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 00:31:57 2018

2 - benign
1 - offensive
0 - hate
"""
import pandas as pd
import os
import pickle
from speechr import TDFClassifierPrepare 

class BagOfWordsClassifier:
    def __init__(self):
        app_path = os.path.dirname(os.path.abspath(__file__))

        self.vectorizer = pickle.load(open(os.path.join(os.path.sep, app_path, 'SimpleTfidfVectorizer.pkl'), 'rb'))
        self.select = pickle.load(open(os.path.join(os.path.sep, app_path, 'Selector.pkl'), 'rb'))
        self.model = pickle.load(open(os.path.join(os.path.sep, app_path, 'SVMModel.pkl'), 'rb'))
    
    def preprocess(self):
        return TDFClassifierPrepare.preprocess

    def analyze(self, text):
        text_array = [text]
        tfidf = self.vectorizer.transform(text_array).toarray()
        X = pd.DataFrame(tfidf)
        
        X_ = self.select.transform(X)
        
        y = self.model.predict(X_)
        
        score = self.scores_to_class_score(y[0])

        return score


    def scores_to_class_score(self, score):
        return {
            2: 0,
            1: 1,
            0: 5
        }[score]
