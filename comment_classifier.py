#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 18:07:05 2018
"""
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.stem.snowball import SnowballStemmer


class CommentClassifier:
    def __init__(self, slurs, violent_words):        
         self.slurs = [s.lower() for s in slurs]
         self.violent_words = [v.lower() for v in violent_words]
         self.analyzer = SentimentIntensityAnalyzer()
         self.stemmer = SnowballStemmer("english")

    
    def analyze(self, text):
        """
        Return a score greater than 0 for text which has an issue
        """
        if text is None:
            return 0
                
        sentiment = self.get_negative_sentiment(text)

        text_array = self.preprocess(text)
        
        slurs = self.get_slur_count(text_array)
        violent_words = self.get_violent_word_count(text_array)
        score = slurs * (violent_words + 1) * (sentiment + 1 )
        return score


    def preprocess(self, text):
        text = nltk.word_tokenize(text)
        text = [self.stemmer.stem(t) for t in text]
        
        
        return text

    def get_negative_sentiment(self, text):
        sentiment = self.analyzer.polarity_scores(text)['neg']
        return sentiment

    def get_slur_count(self, text_array):
        c = 0
        for slur in self.slurs:
            if slur in text_array:
                c += 1
        return c
    
    def get_violent_word_count(self, text_array):
        i = 0
        for violent_word in self.violent_words:
            if violent_word in text_array:
                i += 1
        return i
