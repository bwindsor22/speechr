#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 10:12:22 2018
"""

import pytest
import sqlalchemy
import pandas as pd
import datetime


from speechr import sql_loader
from speechr import config_logging_setup


@pytest.fixture
def DB():
    config_logging_setup.setup_logging()
    app_config = config_logging_setup.get_app_config()
    return sql_loader.SQL_Loader(app_config)

def test_get_engine():
    engine = DB().get_engine()
    assert isinstance(engine, sqlalchemy.engine.base.Engine)

def test_replace():
    d = {'col1': [1, 2], 'col2': [3, 4]}
    expected_df = pd.DataFrame(data=d)
    table = 'test_replace'
    DB().load_df(expected_df, table, 'replace')
    
    df_from_db = DB().read_sql('select * from ' + table + ';')
    assert expected_df.equals(df_from_db)

def test_underscores():
    d = {'col1_underscore': [1, 2], 'col2_underscore': [3, 4]}
    expected_df = pd.DataFrame(data=d)
    table = 'test_underscore'
    DB().load_df(expected_df, table, 'replace')
    
    df_from_db = DB().read_sql('select * from ' + table + ';')
    assert expected_df.equals(df_from_db)
    
def test_dates():
    now = datetime.datetime.now()

    d = {'col1': [now, now], 'col2': [2, 4]}
    expected_df = pd.DataFrame(data=d)
    table = 'test_dates'
    DB().load_df(expected_df, table, 'replace')
    
    df_from_db = DB().read_sql('select * from ' + table + ';')
    assert expected_df.equals(df_from_db)
