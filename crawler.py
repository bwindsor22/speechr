#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 21:35:55 2018

"""
import praw
import itertools
import os
import comment_classifier
import hate_subreddit_finder
import csv
from time import sleep


class Crawler:
    def __init__(self):
        self.reddit = praw.Reddit('bot1')
        
        slurs = self.load_csv_resource('racial_slurs')
        slurs = list(itertools.chain.from_iterable(slurs))
        
        self.CC = comment_classifier.CommentClassifier(slurs)
        
        subreddits_to_scan = self.load_csv_resource('policing_subreddits')
        subreddits_to_scan = list(itertools.chain.from_iterable(subreddits_to_scan))

        self.HRS = hate_subreddit_finder.HateSubredditFinder(self.reddit, subreddits_to_scan)
        
        
    def load_csv_resource(self, file_name):
        app_path = os.path.dirname(os.path.abspath(__file__))
        slurs_file = os.path.join(os.path.sep, app_path, 'ref', file_name) + '.csv'
        slurs = []
        with open(slurs_file, 'r') as file:
            rdr = csv.reader(file)
            for row in rdr:
                slurs.append(row)
        return slurs
                
    def collect(self):
        print('collecting...')
        i = 0
        
        hate_subs = self.HRS.find_hate_subreddits(10)
        print('hate subs: ' + str(hate_subs))
        
        for hate_sub in hate_subs:
            print('--------------------------')
            print('scanning next sub: ' + hate_sub)
            print('--------------------------')
            sleep(1)
        
            try:            
                subreddit = self.reddit.subreddit(hate_sub)
            except:
                print(hate_sub + " is not found")
                continue
            
            submissions = list(subreddit.new(limit=10))
            for sub in submissions:
                sub.comments.replace_more(limit=0)
                for comment in sub.comments.list():
                    i += 1
                    if i % 100 == 0:
                        print('processing comment # ' + str(i))
                    score = self.CC.analyze(comment.body)
                    if score > 0:
                        print(comment.body)
                        print('score: ' + str(score))
        


if __name__ == '__main__':
    c = Crawler()
    c.collect()