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
import pandas as pd
import config_logging_setup

from flask import Flask
app = Flask(__name__)
config_logging_setup.setup_logging()
app_config = config_logging_setup.get_app_config()
DB = sql_loader.SQL_Loader(app_config)

@app.route('/all_comments')
def all_comments():
    return 1

@app.route('/comment_rates')
def comment_rates():
    return 1    

#if __name__ == '__main__':
#    app.run(host='0.0.0.0')