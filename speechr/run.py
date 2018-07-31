#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 21:57:52 2018

@author: bradwindsor
"""


import pandas as pd
import sqlalchemy as sqa


conn_str = "postgresql://p2speechr:speechr123@comments01.cpwa0ujlkpmx.us-east-1.rds.amazonaws.com:5432/comments01"
engine = sqa.create_engine(conn_str, pool_pre_ping=True)

query = "SELECT * FROM pg_catalog.pg_tables;"

a = pd.read_sql(query, engine)