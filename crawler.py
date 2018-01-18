#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 21:35:55 2018

"""
import praw
import itertools
import os
import csv
import datetime
import pandas as pd
import numpy as np

import comment_classifier
import hate_subreddit_finder
import sql_loader

class Crawler:
    def __init__(self):
        self.reddit = praw.Reddit('bot1')
        
        slurs = self.load_csv_resource('racial_slurs')
        slurs = list(itertools.chain.from_iterable(slurs))

        violent_words = self.load_csv_resource('violent_words')
        violent_words = list(itertools.chain.from_iterable(violent_words))
        
        self.CC = comment_classifier.CommentClassifier(slurs, violent_words)
        
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
        
        hate_subs = self.HRS.find_unique_hate_subreddits(10)
        print('hate subs: ' + str(hate_subs))
        
        columns = ['comment_id', 'created_utc', 'permalink', 'subreddit', 'vote_score',  'body', 'classifier_score']
        self.potential_hate_comments = pd.DataFrame(data=np.zeros((0,len(columns))), columns=columns)

        for hate_sub in hate_subs:
            print('--------------------------')
            print('scanning next sub: ' + hate_sub)
            print('--------------------------')
                    
            subreddit = self.reddit.subreddit(hate_sub)

            try:            
                submissions = list(subreddit.new(limit=3))

                for sub in submissions:
                    sub.comments.replace_more(limit=0)
                    for comment in sub.comments.list():
                        i += 1
                        if i % 100 == 0:
                            print('processing comment # ' + str(i))
                        score = self.CC.analyze(comment.body)
                        if score > 0:
                            time = datetime.datetime.utcfromtimestamp( comment.created_utc )
                            temp_df = pd.DataFrame([[comment.id, time, comment.permalink, hate_sub, \
                                                     comment.score, comment.body, score]], \
                                                   columns=columns)
                            self.potential_hate_comments.append(temp_df, ignore_index=True)
                            print(comment.body)
                            print('score: ' + str(score))
            except: 
                print("error processing " + hate_sub)

    def load_to_db(self):
        DB = sql_loader.SQL_Loader()
        
        hate_sub_reports = self.HRS.get_hate_sub_reports(-1)
        DB.load_df(hate_sub_reports, 'hate_sub_reports', 'append')

        DB.load_df(self.potential_hate_comments, 'comments', 'append')


    def run(self):
        self.collect()
        self.load_to_db()
        
if __name__ == '__main__':
    c = Crawler()
    c.run()