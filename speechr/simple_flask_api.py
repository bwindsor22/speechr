#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 21:56:25 2018
export FLASK_APP=simple_flask_api.py
flask run --host=0.0.0.0
http://<ipv4publicip>:5000/
"""

import json
import sql_loader
import os
import pandas as pd

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    
    app_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(os.path.sep, app_path, 'config', 'app_config') + '.json'
    if os.path.exists(config_path):
        with open(config_path, 'rt') as f:
            config = json.load(f)
    
    s = sql_loader.SQL_Loader(config)
    
    sql = '''
        select *
        from comments
        order by created_utc desc'''
    
    engine = s.get_engine()
    df = pd.read_sql(sql, engine)
    return df.to_json(orient='records')

