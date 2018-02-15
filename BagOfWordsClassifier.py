#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 00:31:57 2018
"""
import pandas as pd
import joblib 

class BagOfWordsClassifier:
    def __init__(self):
        #self.vectorizer = joblib.load('SimpleTfidfVectorizer.pkl')
        self.selector = joblib.load('Selector.pkl')
        self.model = joblib.load('SVMModel.pkl')
    
    def classify(self, text):
        tfidf = self.vectorizer.fit_transform(text).toarray()
        X = pd.DataFrame(tfidf)

        X_ = self.select.transform(X)
        
        y_pred = self.model.predict(X_)
        return y_pred


