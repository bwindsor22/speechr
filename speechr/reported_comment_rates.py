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
        results = self.get_percent_and_scanned_total(raw_table)
        
        results[Endpoints.rolling_total_hate] = self.get_rolling_total(raw_table)
        
        return results

    def get_raw_table(self):
        sql = '''
        with base as ( 
            select subreddit, 
                    date(time_scanned) date_scanned,
                    sum(comments_scanned) as total_scanned,
                    sum(keyword_hate_comments) as total_keyword_hate,
                    sum(bow_hate_comments) as total_bow_hate
            from comment_count_per_subreddit 
            where time_scanned >= date_trunc('day', NOW() - interval '2 months')
            group by subreddit, date_scanned
        )
        select subreddit, date_scanned, total_scanned, 
                total_keyword_hate, 
                total_keyword_hate / total_scanned as "percent_keyword_hate",
                total_bow_hate,
                total_bow_hate / total_scanned as "percent_bow_hate"
        from base;
        '''
        return self.DB.read_sql(sql)
    
    def get_percent_and_scanned_total(self, raw_table):
        results = {}

        results[Endpoints.total_scanned] = \
            pd.pivot_table(raw_table, values='total_scanned', index=['date_scanned'], columns=['subreddit'])

        results[Endpoints.percent_keyword_hate] = \
            pd.pivot_table(raw_table, values='percent_keyword_hate', index=['date_scanned'], columns=['subreddit'])
            
        results[Endpoints.percent_bow_hate] = \
            pd.pivot_table(raw_table, values='percent_bow_hate', index=['date_scanned'], columns=['subreddit'])
        
        for name, vals in results.items():
            results[name]['date'] = vals.index.astype(str)
            
        return results
    
    def get_rolling_total(self, raw_table):
        grouped = raw_table.groupby('subreddit').sum()
        grouped['subreddit'] = grouped.index.astype(str)
        grouped = grouped[['subreddit', 'total_bow_hate', 'total_keyword_hate']]
        return grouped
        
        
    