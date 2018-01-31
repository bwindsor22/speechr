#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 17:23:55 2018

"""
import pandas as pd
import sqlalchemy as sqa
from sqlalchemy import text

class SQL_Loader():
    def __init__(self):
        user = 'sys_speechr'
        passwd = 'pass'
        host = 'localhost'
        port =5432
        db_name = 'example'
        
        conn_str = "postgresql://{}:{}@{}:{}/{}".format(user, passwd, host, port, db_name)
        
        #e.g. 'postgresql://sys_speechr:pass@localhost:5432/example'
        self.engine = sqa.create_engine(conn_str)

    def insert_dict(self, data, table_name, cols):
        data = pd.DataFrame(data, index=[0]).transpose()
        data.columns = cols
        data.table_na
    
    def load_df(self, data, table_name, exists):
        data.to_sql( table_name, self.engine, if_exists = exists, index=False)
        
    def pull_sub_log(self): # return scanned sub log
        db = SQL_Loader()
        
        sql = text('select subreddit,max("time_ran_utc") from scanned_log group by subreddit') # eventually make this smarter, i.e. pull entry only if most recent
        result = db.engine.execute(sql)
        
        subreddit = []
        dates = []
        
        for _ in result:
            dates.append(_[1])
            subreddit.append(_[0])
            
        dict_log = dict(zip(subreddit,dates))
        
        return dict_log