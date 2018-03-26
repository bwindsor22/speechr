# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 19:19:43 2018

@author: CSL
"""

from speechr import sql_loader
from speechr import config_logging_setup

import pandas as pd
import numpy as np

class Comment_Rates():
    def __init(self):
        app_config = config_logging_setup.get_app_config()
        self.DB = sql_loader.SQL_Loader(app_config)
        
    
    # target data table = user/#comments_posted/avg_bow_scores/avg_keyword_score
    
    def get_users(self): # table 
        sql = """select comments.comment_id, comments.author, bow_scores.score as bow_score, keyword_scores.score as keyword_score
        from comments, bow_scores, keyword_scores 
        where comments.comment_id = bow_scores.comment_id 
        and (bow_scores.score >=5 or keyword_scores.score >=5);"""
        
        toxic_user_report_cols = ['comment_id', 'user', 'bow_score', 'keyword_score']
        self.toxic_user_report = pd.DataFrame(data=np.zeros((0,len(toxic_user_report_cols))), columns=toxic_user_report_cols)
        
        report = self.DB.toxic_user()
        
        # temp_df = pd.DataFrame([[comment_id, user,bow_score, ]], columns=comment_count_per_scan_cols)
    
        self.toxic_user_report = self.toxic_user_report.append(report, ignore_index = True)
        
        
