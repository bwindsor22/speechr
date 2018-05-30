#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 00:38:47 2018
"""

import re
import logging
import pandas as pd
import numpy as np
import datetime


import sql_loader
import config_logging_setup

from speechr import resource_loader

class HateSubredditFinder:
    def __init__(self, reddit):
        self.logger = logging.getLogger('default')
        self.reddit = reddit
        self.subreddits_to_scan = resource_loader.load_csv_resource_to_list('policing_subreddits')
        self.collected = False
        
        self.app_config = config_logging_setup.get_app_config()
        self.SQL = sql_loader.SQL_Loader(self.app_config)
        
    def find_unique_hate_subreddits(self, lim):
        if not self.collected:
            self.collect_hate_subreddit_submissions(lim)
            self.collected = True
            
        archive_subs = self.get_subs_from_log()
        unique_subs = self.hate_sub_reports.subreddit_linked.unique()
        unique_subs = unique_subs.tolist()
        
        if archive_subs is not None:
            archive_subs_set = set(archive_subs)
            unique_subs_set = set(unique_subs)
            archive_unique_subs = archive_subs_set - unique_subs_set
            
            return unique_subs + list(archive_unique_subs)
        else:
            return unique_subs

    def get_hate_sub_reports(self, lim):
        if not self.collected:
            self.collect_hate_subreddit_submissions(lim)
            self.collected = True
        return self.hate_sub_reports

    def collect_hate_subreddit_submissions(self,lim):
        """
        Identifies subreddits which are likely to contain hate speech
        """        
        
        columns = ['submission_id', 'created_utc', 'place_submitted','subreddit_linked', 'vote_score', 'title', 'permalink']
        self.hate_sub_reports = pd.DataFrame(data=np.zeros((0,len(columns))), columns=columns)
        
        for to_scan in self.subreddits_to_scan:        
            subreddit = self.reddit.subreddit(to_scan)
            for sub in subreddit.hot(limit=lim):
                if re.search("reddit.com/r/", sub.url, re.IGNORECASE):
                    url_parts = sub.url.split("/")
                    
                    if url_parts[3] == "r" and len(url_parts) > 3:
                        hate_sub = url_parts[4].lower()
                        
                        #not r/againsthatesubreddits or r/internethitlers
                        if hate_sub not in self.subreddits_to_scan:
                            
                            time = datetime.datetime.utcfromtimestamp(sub.created_utc)
                            temp_df = pd.DataFrame([[sub.id, time, to_scan, hate_sub, sub.score, sub.title, sub.permalink]], \
                                                   columns=columns)
                            self.hate_sub_reports = self.hate_sub_reports.append(temp_df, ignore_index=True)   
                else:
                    self.logger.info("This link has no associated subreddit: {}".format(sub.url))
    
        
    def get_subs_from_log(self):
        cmd = """select subreddit, max(time_ran_utc) from scanned_log 
        where now()::timestamp - time_ran_utc < interval '1 day' group by subreddit"""

        result = self.SQL.subs_from_log()
        return result
    
        # lists only subreddit
        """select distinct(subreddit) from scanned_log where current_date - time_ran_utc < interval '1 day';"""
        