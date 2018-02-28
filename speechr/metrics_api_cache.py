#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 14:43:22 2018

Pre-loads items from database into in-memory json strings for use with flask api
"""
import logging

from speechr import sql_loader
from speechr import config_logging_setup


class Metrics_api_cache():
    def __init__(self):
        app_config = config_logging_setup.get_app_config()
        self.DB = sql_loader.SQL_Loader(app_config)
        self.logger = logging.getLogger('cache')


    def setup_cache(self):
        cache = {}                        
        
        statements = self.get_sql_statements()
        
        for metric, sql in statements.items():
            cache[metric] = self.sql_to_json(sql)
        
        self.logger.info('Refreshed cache')
        
        return cache
    
    def sql_to_json(self, sql):
        df = self.DB.read_sql(sql)
        return df.to_json(orient='records')



    def get_sql_statements(self):
        statements = {}
        
        statements['all_comments'] = '''
                select *
                from comments
                order by created_utc desc;
                '''
        statements['comment_rates'] = '''
                select *
                from comment_count_per_subreddit
                order by time_scanned desc;
                '''
        return statements