#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 17:10:21 2018
"""

import json

import psycopg2 as pg
import sqlalchemy as sqa
import pandas as pd


with open('config.json') as f:
    conf = json.load(f)
    conn_str = "host={} dbname={} user={} password={}".format(host, database, user, passw)

    engine = sqa.create_engine('postgresql://sys_speechr:pass@localhost:5432/example')
