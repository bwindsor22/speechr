#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 00:31:57 2018

2 - benign
1 - offensive
0 - hate
"""
import pandas as pd
import pickle
from TDFClassifierPrepare import preprocess

class BagOfWordsClassifier:
    def __init__(self):
        self.vectorizer = pickle.load(open("SimpleTfidfVectorizer.pkl", "rb"))
        self.select = pickle.load(open("Selector.pkl", "rb"))
        self.model = pickle.load(open("SVMModel.pkl", "rb"))
    
    def classify(self, text_array):
        tfidf = self.vectorizer.transform(text_array).toarray()
        X = pd.DataFrame(tfidf)
        
        X_ = self.select.transform(X)
        
        y_pred = self.model.predict(X_)
        return y_pred


