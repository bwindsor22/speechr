#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 00:38:47 2018

"""

import praw
import re
import logging


def find_hate_subreddits(subreddits_to_scan, lim):
    """
    Identifies subreddits which are likely to contain hate speech
    :param subreddits_to_scan: forums where hate subreddits are frequently reported
    """        
    hate_subs = {}

    for to_scan in subreddits_to_scan:        
        subreddit = reddit.subreddit(to_scan)
        for sub in subreddit.hot(limit=lim):
            if re.search("reddit.com/r/", sub.url, re.IGNORECASE):
                url_parts = sub.url.split("/")
                
                if url_parts[3] == "r" and len(url_parts) > 3:
                    hate_sub = url_parts[4].lower()
                    if hate_sub not in subreddits_to_scan:                        
                        if hate_sub in hate_subs:
                            hate_subs[hate_sub] = hate_subs[hate_sub] + 1
                        else:
                            hate_subs[hate_sub] = 1
                    
            else:
                logging.info("This link has no associated subreddit: {}".format(sub.url))
        
    return(hate_subs)


reddit = praw.Reddit('bot1')

subreddits_to_scan = ['againsthatesubreddits', 'antisemitismwatch', 'internethitlers']
lim = 20

potential_hate_subs  = find_hate_subreddits(subreddits_to_scan, lim)

logging.info(potential_hate_subs)