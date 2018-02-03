#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 21:35:55 2018

"""
import praw
from prawcore.exceptions import NotFound

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
        self.number = 5
        self.offset = datetime.timedelta(2)
        
        
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
        
        hate_subs = self.HRS.find_unique_hate_subreddits(self.number)
        print('hate subs: ' + str(hate_subs))

        Takeoff = sql_loader.SQL_Loader()
        Quavo = Takeoff.pull_sub_log()

        columns = ['comment_id', 'created_utc', 'permalink','subreddit', 'vote_score', 'body', 'classifier_score']
        self.potential_hate_comments = pd.DataFrame(data=np.zeros((0,len(columns))), columns=columns)
        
        for hate_sub in hate_subs:
            print('--------------------------')
            print('scanning next sub: ' + hate_sub)
            print('--------------------------')
                    
            subreddit = self.reddit.subreddit(hate_sub)

            try:            
                submissions = list(subreddit.new(limit=10))
                for sub in submissions:
                    sub.comments.replace_more(limit=0)
                    for comment in sub.comments.list():
                        i += 1
                        if i % 100 == 0:
                            print('processing comment # ' + str(i))
                        score = self.CC.analyze(comment.body)
                        
                        # print(scanned_log.get(hate_sub))
                        # if score > 0:
                        if score > 0 and \
                        datetime.datetime.utcfromtimestamp(comment.created_utc)> Quavo.get(hate_sub) - self.offset:
                            time = datetime.datetime.utcfromtimestamp( comment.created_utc )
                            temp_df = pd.DataFrame([[comment.id, \
                                                     time, \
                                                     comment.permalink, \
                                                     hate_sub, \
                                                     comment.score, \
                                                     comment.body, \
                                                     score]], 
                                                   columns=columns)
                            self.potential_hate_comments = self.potential_hate_comments.append(temp_df, ignore_index=True)
                            print(comment.body)
                            print('score: ' + str(score))
            except NotFound as ex:
                print('Subreddit {} not found'.format(hate_sub))
            except Exception as e:
                print('Error processing sub: {}, {}'.format(hate_sub, e))

    def load_to_db(self):
        DB = sql_loader.SQL_Loader()
        
        hate_sub_reports = self.HRS.get_hate_sub_reports(-1)
        DB.load_df(hate_sub_reports, 'hate_sub_reports', 'append')
        
        print(self.potential_hate_comments)
        DB.load_df(self.potential_hate_comments, 'comments', 'append')
        
        print(self.scanned_hate_subs)
        DB.load_df(self.scanned_hate_subs, 'scanned_log', 'append')

    def run(self):
        self.collect()
        self.log_current_run()
        self.load_to_db()

    def log_current_run(self):
        time_run = datetime.datetime.utcnow()
        
        scanned_hate_subs = self.HRS.find_unique_hate_subreddits(self.number) # need to figure out how to match with
        columns = ['time_ran_utc', 'subreddit']
        self.scanned_hate_subs = pd.DataFrame(data=np.zeros((0,len(columns))), columns=columns)
        
        for _ in scanned_hate_subs:
            temp_df = pd.DataFrame([[
                    time_run,
                    _]],
                    columns=columns)
            self.scanned_hate_subs = self.scanned_hate_subs.append(temp_df, ignore_index=True)


if __name__ == '__main__':
    c = Crawler()
    c.run()    
    