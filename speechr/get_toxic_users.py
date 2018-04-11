# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 19:19:43 2018

@author: CSL
"""

from speechr import sql_loader
from speechr import config_logging_setup

import pandas as pd
import numpy as np

class Toxic_Users():
    def __init__(self):
        app_config = config_logging_setup.get_app_config()
        self.DB = sql_loader.SQL_Loader(app_config)
        
    
    # target data table = user/#comments_posted/avg_bow_scores/avg_keyword_score
    
    def get_users(self): # table 
        raw_table = self.get_raw_table()
        print(raw_table)
        
    def get_raw_table(self):
        
        sql = """
            WITH temp AS(
            SELECT comment_id, MAX(score) as bow_score FROM bow_scores
            GROUP BY comment_id
            ), 
            temp1 AS(
            SELECT comment_id, MAX(score) as keyword_score FROM keyword_scores
            GROUP BY comment_id
            )
            SELECT DISTINCT comments.author AS author, comments.comment_id as comment_id, temp.bow_score as bow_score,
            temp1.keyword_score as keyword_score, comments.created_utc AS created_utc
            
            FROM comments
            INNER JOIN temp ON (comments.comment_id = temp.comment_id and temp.bow_score >= 5)
            INNER JOIN temp1 ON (comments.comment_id = temp1.comment_id)
            ;
        """

        return self.DB.execute_sql(sql)
    
    def store_data(self):
        
        toxic_user_report_cols = ['comment_id', 'user', 'bow_score', 'keyword_score', 'created_utc']
        self.toxic_user_report = pd.DataFrame(data=np.zeros((0,len(toxic_user_report_cols))), columns=toxic_user_report_cols)
        
        report = self.get_raw_table()
        #print(report.rowcount, "comments found from the following SQL query")
        
        temp_time = self.most_recent_scan_time()
        temp_time1 = temp_time.iloc[0]
        reference_time = temp_time1[0]
        
        if not reference_time:
            for _ in report:
                temp_df = pd.DataFrame([[_[0], _[1], _[2], _[3], _[4]]], columns=toxic_user_report_cols)
                self.toxic_user_report = self.toxic_user_report.append(temp_df, ignore_index = True)
        else:
            for _ in report:
                if _[4]-reference_time:
                    temp_df = pd.DataFrame([[_[0], _[1], _[2], _[3], _[4]]], columns=toxic_user_report_cols)
                    self.toxic_user_report = self.toxic_user_report.append(temp_df, ignore_index = True)
                                        
        # add load DB, need to account for remove duplicates
        self.DB.load_df(self.toxic_user_report, 'toxic_user_report','append')
        
    def most_recent_scan_time(self):
        sql = """SELECT MAX(time_ran_utc) from scanned_log;"""
        
        return self.DB.read_sql(sql)
        
    def run(self):
        self.get_users()
        self.store_data()
        
        
"""if __name__ == "__main__":
    b = Toxic_Users()
    b.run()"""