#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 18:07:05 2018
"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 


class CommentClassifier:
    def __init__(self, slurs):        
         self.slurs = slurs
         self.analyzer = SentimentIntensityAnalyzer()
    
    def analyze(self, text):
        """
        Return a score greater than 0 for text which has an issue
        """
        if text is None:
            return 0
        
        #text = text.encode('ascii',errors='ignore')
        sentiment = self.get_negative_sentiment(text)
        slurs = self.get_slur_count(text)
        return slurs * sentiment

    def get_negative_sentiment(self, text):
        sentiment = self.analyzer.polarity_scores(text)['neg']
        return sentiment + 1

    def get_slur_count(self, text):
        c = 0
        for slur in self.slurs:
            if slur.lower() in text.lower():
                c += 1
        return c
    

