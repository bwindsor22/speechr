#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 17:23:55 2018

"""
import pandas as pd
import logging
import sqlalchemy as sqa
from sqlalchemy import text

class SQL_Loader():
    def __init__(self, app_config):
        self.logger = logging.getLogger('default')

        DB = app_config['DB']
        user = DB['user']
        passwd = DB['passwd']
        host = DB['host']
        port = DB['port']
        db_name = DB['db_name']
        
        conn_str = "postgresql://{}:{}@{}:{}/{}".format(user, passwd, host, port, db_name)
        
        #e.g. 'postgresql://sys_speechr:pass@localhost:5432/example'
        self.engine = sqa.create_engine(conn_str, pool_pre_ping=True)
        
    def get_engine(self):
        return self.engine
    
    def insert_dict(self, data, table_name, cols):
        data = pd.DataFrame(data, index=[0]).transpose()
        data.columns = cols
        data.table_na
    
    def load_df(self, data, table_name, exists):
        if data.empty or data is None:
            self.logger.info('Skipping db load for empty df: {}'.format(table_name))
            return
        data.to_sql( table_name, self.engine, if_exists = exists, index=False)
        
    
    def read_sql(self, sql):
        return pd.read_sql(sql, self.engine)
    
    def execute_sql(self, sql_text):
        sql = text(sql_text)
        try:
            result = self.engine.execute(sql)
        except Exception as e:
            self.logger.error("Error executing statement {}".format(e))
            self.logger.exception(e)
            return None
        return result
    
    def pull_sub_log(self):        
        text = 'select subreddit,max("time_ran_utc") from scanned_log group by subreddit'
        place_holder = []
        
        try:
            df = self.execute_sql(text)
        except Exception as e:
            self.logger.error("error pulling scanned log history")
            return place_holder
            
        if df is not None:
            return self.sub_log_to_dict(df)
        
    def subs_from_log(self):
        text = """select subreddit, max(time_ran_utc) from scanned_log 
        where now()::timestamp - time_ran_utc < interval '1 day' group by subreddit"""
        place_holder = []
        
        try:
            df = self.execute_sql(text)
        except Exception as e:
            self.logger.error("error pulling subs from scanned log history")
            return place_holder
        
        if df is not None:
            return self.sql_df_to_array(df,0)
        
    def sub_log_to_dict(self, result):
        subreddit, dates = [], []
        
        for _ in result:
            dates.append(_[1])
            subreddit.append(_[0])
            
        dict_log = dict(zip(subreddit,dates))
        
        return dict_log
    
    def sql_df_to_array (self,result,i):
        # where i = target column in df
        data = []
        
        for _ in result:
            data.append(_[i])
        
        return data
