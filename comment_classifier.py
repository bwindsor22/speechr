#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 18:07:05 2018
"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class CommentClassifier:
    def __init__(self, slurs, violent_words):        
         self.slurs = slurs
         self.violent_words = violent_words
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
        violent_words = self.get_violent_word_count(text)
        return slurs * violent_words * sentiment

    def get_negative_sentiment(self, text):
        sentiment = self.analyzer.polarity_scores(text)['neg']
        return sentiment + 1

    def get_slur_count(self, text):
        c = 0
        # can we improve the runtime of this?  Or is it necessary, looks like N^2 runtime?
        for slur in self.slurs:
            if slur.lower() in text.lower():
                c += 1
        return c
    
    def get_violent_word_count(self,text):
        i = 0
        for violent_word in self.violent_words:
            if violent_word.lower() in text.lower():
                i += 1
        return i
