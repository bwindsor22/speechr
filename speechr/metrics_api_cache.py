#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 14:43:22 2018

Pre-loads items from database into in-memory json strings for use with flask api
"""
import logging
from speechr import sql_loader
from speechr import config_logging_setup
from speechr.endpoints_enum import Endpoints
from multiprocessing import Manager


class Cache_Helper():
    def __init__(self):
        app_config = config_logging_setup.get_app_config()
        self.DB = sql_loader.SQL_Loader(app_config)
        self.logger = logging.getLogger('cache')
        
        self.prerequisite_tables = ['comments'] #, 'comment_count_per_subreddit']
        
        manager = Manager()
        self.cache = manager.dict()


    def refresh_cache(self):
        statements = self.get_sql_statements()

        for metric, sql in statements.items():
            self.cache[metric] = self.sql_to_json(sql)

        self.cache[Endpoints.times_refreshed] = self.increment_refresh_count()
    
        self.logger.info('Refreshed cache')

        return self.cache

    def increment_refresh_count(self):
        '''
        All values in cach must be strings
        '''
        if Endpoints.times_refreshed in self.cache.keys():
            refreshed = int(self.cache[Endpoints.times_refreshed])
            return str( refreshed + 1 )
        else:
           return '1'       

    def sql_to_json(self, sql):
        df = self.DB.read_sql(sql)
        return df.to_json(orient='records')

    def get_sql_statements(self):
        statements = {}

        statements[Endpoints.all_comments] = '''
                select *
                from comments
                order by created_utc desc;
                '''
        statements[Endpoints.comment_rates] = '''
                select *
                from comment_count_per_subreddit
                order by time_scanned desc;
                '''
        return statements
    
    def prerequisite_tables_exist(self):
        for table in self.prerequisite_tables:
            statement = '''
            select exists (
                select 1
                from information_schema.tables
                where table_name = '{}' 
            )    
            '''.format(table)
            exists_tbl = self.DB.read_sql(statement)
            if not (exists_tbl.shape[0] > 0 and exists_tbl.values[[0]]):
                return False
        return True
