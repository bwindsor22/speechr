#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 21:35:55 2018

"""
import praw
from prawcore.exceptions import NotFound
from prawcore.exceptions import Forbidden

import datetime
import pandas as pd
import numpy as np
import logging

import config_logging_setup
import hate_subreddit_finder
import sql_loader
import config_logging_setup


class Crawler:
    """
    Pulls comments from praw's rest API
    F
    """
    def __init__(self):
        self.logger = logging.getLogger('default')

        self.app_config = config_logging_setup.get_app_config()
        self.logger.info('loaded config {}'.format(self.app_config))

        self.reddit = praw.Reddit(self.app_config['reddit_bot'])

        self.HRS = hate_subreddit_finder.HateSubredditFinder(self.reddit)
        self.number_of_hate_subs = self.app_config['crawler']['num_hate_subs']
        self.offset = datetime.timedelta(self.app_config['crawler']['time_delta_in_days'])

        self.DB = sql_loader.SQL_Loader(self.app_config)

        self.subreddit_last_scanned_dates = self.DB.pull_sub_log()

    def collect(self):
        self.logger.info('collecting...')
        potential_hate_subreddits = self.HRS.find_unique_hate_subreddits(self.number_of_hate_subs)
        self.logger.info('hate subs: ' + str(potential_hate_subreddits))

        comment_count_cols = ['subreddit', 'time_scanned', 'comments_scanned']
        comment_count_per_scan = pd.DataFrame(data=np.zeros((0, len(comment_count_cols))), columns=comment_count_cols)

        for subreddit_name in potential_hate_subreddits:
            self.logger.info('--------------------------')
            self.logger.info('scanning next subreddit: ' + subreddit_name)
            self.logger.info('--------------------------')

            subreddit_comment_counter = 0
            subreddit = self.reddit.subreddit(subreddit_name)
            try:
                subreddit_scan_time = datetime.datetime.utcnow()

                last_scan_time = self.get_last_scan(subreddit_name)
                self.logger.info('last scan time {} '.format(str(last_scan_time)))
                subreddit_comments = []

                submissions = list(subreddit.new(limit=50))

                for submission in submissions:
                    if datetime.datetime.utcfromtimestamp(submission.created_utc) > last_scan_time - self.offset:
                        submission.comments.replace_more(limit=100)
                        comment_list = submission.comments.list()
                        self.logger.info('.. found {} comments'.format(len(comment_list)))

                        subreddit_comment_counter += len(comment_list)

                        subreddit_comments.extend(comment_list)

                #Processor.process(subreddit_comments)
                self.load_comments_to_db(subreddit_comments, subreddit_scan_time)
                self.log_subreddit_processed(subreddit, subreddit_scan_time)

            except NotFound:
                self.logger.info('Subreddit {} not found'.format(subreddit_name))
            except Forbidden:
                self.logger.info('Subreddit {} forbidden'.format(subreddit_name))
            except Exception:
                self.logger.exception('Error processing sub: {}'.format(subreddit_name))

            comment_count_per_scan = self.append_comment_counts(subreddit_name, comment_count_per_scan, subreddit_comment_counter, comment_count_cols)

        self.record_comment_count(comment_count_per_scan)

    def append_comment_counts(self, hate_sub, comment_count_per_scan, comments_scanned, cols):
        sub_comment_count = pd.DataFrame([[hate_sub, datetime.datetime.utcnow(), comments_scanned]], columns=cols)
        sub_comment_count = sub_comment_count.reset_index(drop=True)

        comment_count_per_scan = pd.concat([comment_count_per_scan, sub_comment_count], axis=0)

        return comment_count_per_scan

    def record_comment_count(self, comment_count_per_scan):
        self.DB.load_df(comment_count_per_scan, 'comment_count_per_subreddit', 'append')

    def load_comments_to_db(self, subreddit_comments, subreddit_scan_time):
        columns = ['id','author', 'created_utc', 'permalink','subreddit', 'vote_score', 'body', 'time_analyzed']
        comments_list = []
        for comment in subreddit_comments:
            author = ""
            if comment.author is not None:
                author = comment.author.name
            comments_list.append([comment.id, author, comment.created_utc, comment.permalink,
                                            comment.subreddit.display_name, comment.score, comment.body, subreddit_scan_time])
        comments_df = pd.DataFrame(comments_list, columns=columns)
        self.DB.load_df(comments_df, 'comments', 'append')

    def log_subreddit_processed(self, subreddit, subreddit_scan_time):
        self.logger.info('recording subreddit {} processed at {}...'.format(subreddit, subreddit_scan_time))

        columns = ['time_ran_utc', 'subreddit']
        scanned_hate_subs = pd.DataFrame([[subreddit_scan_time, subreddit.display_name]], columns=columns)

        self.DB.load_df(scanned_hate_subs, 'scanned_log', 'append')

    def log_hate_sub_reports(self):
        hate_sub_reports = self.HRS.get_hate_sub_reports(-1)
        self.DB.load_df(hate_sub_reports, 'hate_sub_reports', 'append')

    def get_last_scan(self, subreddit):
        if self.subreddit_last_scanned_dates is None:
            return datetime.datetime.min + self.offset

        if self.subreddit_last_scanned_dates.get(subreddit) is None:
            return datetime.datetime.min + self.offset
        else:
            return self.subreddit_last_scanned_dates.get(subreddit)

    def run(self):
        self.collect()
        self.log_hate_sub_reports()
        self.logger.info("...finished")

if __name__ == "__main__":
 config_logging_setup.setup_logging()
 b = Crawler()
 b.run()
