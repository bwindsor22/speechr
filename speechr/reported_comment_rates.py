#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 23:17:01 2018
"""
from speechr import sql_loader
from speechr import config_logging_setup
from speechr.endpoints_enum import Endpoints

import pandas as pd

class Comment_Rates():
    def __init__(self):
        app_config = config_logging_setup.get_app_config()
        self.DB = sql_loader.SQL_Loader(app_config)
        

    def get_results(self):
        raw_table = self.get_raw_table()
        pivots = self.pivot_tables(raw_table)
        return pivots

    def get_raw_table(self):
        sql = '''
        with base as ( 
            select subreddit, 
                    date(time_scanned) date_scanned,
                    sum(comments_scanned) as total_scanned,
                    sum(keyword_hate_comments) as keyword_hate,
                    sum(bow_hate_comments) as bow_hate
            from comment_count_per_subreddit 
            group by subreddit, date_scanned
        )
        select subreddit, date_scanned, total_scanned, 
                keyword_hate, keyword_hate / total_scanned as "%%_keyword_hate",
                bow_hate, bow_hate / total_scanned as "%%_bow_hate"
        from base;
        '''
        return self.DB.read_sql(sql)
    
    def pivot_tables(self, df):
        pivots = {}
        pivots[Endpoints.total_scanned] = \
            pd.pivot_table(df, values='total_scanned', index=['date_scanned'], columns=['subreddit'])
        pivots[Endpoints.percent_keyword_hate] = \
            pd.pivot_table(df, values='%_keyword_hate', index=['date_scanned'], columns=['subreddit'])
        pivots[Endpoints.percent_bow_hate] = \
            pd.pivot_table(df, values='%_bow_hate', index=['date_scanned'], columns=['subreddit'])
        
        for name, vals in pivots.items():
            pivots[name]['date'] = vals.index.astype(str)
        return pivots
        
    