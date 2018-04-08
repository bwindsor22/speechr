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
        
        sql = """ WITH temp AS
        ( 
        SELECT comments.author AS author, comments.comment_id AS comment_id, bow_scores.score AS bow_score, 
        comments.created_utc AS created_utc 
        FROM comments 
        INNER JOIN bow_scores ON (comments.comment_id = bow_scores.comment_id and bow_scores.score >=5)
        )
        SELECT temp.author, temp.comment_id, temp.bow_score, keyword_scores.score as keyword_score, temp.created_utc
        FROM keyword_scores
        INNER JOIN temp ON (temp.comment_id = keyword_scores.comment_id)
        ;"""
        
        """SELECT temp.author, temp.comment_id, temp.bow_score, keyword_scores.score as keyword_score, temp.created_utc
        FROM temp
        INNER JOIN keyword_scores ON (temp.comment_id = keyword_scores.comment_id and keyword_scores.score >=5)"""
        #and  now()::timestamp - comments.created_utc < interval '1 days';"""
        
        return self.DB.execute_sql(sql)
    
    def store_data(self):
        
        toxic_user_report_cols = ['comment_id', 'user', 'bow_score', 'keyword_score']
        self.toxic_user_report = pd.DataFrame(data=np.zeros((0,len(toxic_user_report_cols))), columns=toxic_user_report_cols)
        
        report = self.get_raw_table()
        print(report.rowcount, "comments found from the following SQL query")
        
        for _ in report:
            temp_df = pd.DataFrame([[_[0], _[1], _[2], _[3]]], columns=toxic_user_report_cols)
    
            self.toxic_user_report = self.toxic_user_report.append(temp_df, ignore_index = True)
                        
        # add load DB, need to account for remove duplicates
        self.DB.load_df(self.toxic_user_report, 'toxic_user_report','append')
        
    def run(self):
        self.get_users()
        self.store_data()
        
        
if __name__ == "__main__":
    b = Toxic_Users()
    b.run()