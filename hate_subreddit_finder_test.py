#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 19:48:56 2018
"""
import unittest
import praw
import hate_subreddit_finder

class TestCommentClassifier(unittest.TestCase):
    def setUp(self):
        reddit = praw.Reddit('bot1')
        subreddits_to_scan = ['againsthatesubreddits', 'antisemitismwatch', 'internethitlers']
        self.HRS = hate_subreddit_finder.HateSubredditFinder(reddit, subreddits_to_scan)
        
    
    def test_HRS(self):
        lim = 20
        hate_subs = self.HRS.find_hate_subreddits(lim)
        print(hate_subs)
        self.assertLess(0, len(hate_subs))
        
if __name__ == '__main__':
    unittest.main()
