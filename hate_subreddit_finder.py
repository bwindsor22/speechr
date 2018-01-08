#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 00:38:47 2018
"""

import re
import logging

class HateSubredditFinder:
    def __init__(self, reddit, subreddits_to_scan):   
        self.reddit = reddit
        self.subreddits_to_scan = subreddits_to_scan


    def find_hate_subreddits(self,lim):
        """
        Identifies subreddits which are likely to contain hate speech
        """        
        hate_subs = {}
    
        for to_scan in self.subreddits_to_scan:        
            subreddit = self.reddit.subreddit(to_scan)
            for sub in subreddit.hot(limit=lim):
                if re.search("reddit.com/r/", sub.url, re.IGNORECASE):
                    url_parts = sub.url.split("/")
                    
                    if url_parts[3] == "r" and len(url_parts) > 3:
                        hate_sub = url_parts[4].lower()
                        if hate_sub not in self.subreddits_to_scan:                        
                            if hate_sub in hate_subs:
                                hate_subs[hate_sub] = hate_subs[hate_sub] + 1
                            else:
                                hate_subs[hate_sub] = 1
                        
                else:
                    logging.info("This link has no associated subreddit: {}".format(sub.url))
        
        logging.info("found potential hate subs" + str(hate_subs) )
            
        return(hate_subs)


