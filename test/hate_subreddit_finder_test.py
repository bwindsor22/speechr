#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 19:48:56 2018
"""
import pytest
import praw
from speechr import hate_subreddit_finder

def HRS():
    reddit = praw.Reddit('bot1')
    subreddits_to_scan = ['againsthatesubreddits', 'antisemitismwatch', 'internethitlers']
    return hate_subreddit_finder.HateSubredditFinder(reddit, subreddits_to_scan)
    

def test_HRS():
    lim = 20
    hate_subs = HRS().find_unique_hate_subreddits(lim)
    print(hate_subs)
    assert 0 < hate_subs.size
    
