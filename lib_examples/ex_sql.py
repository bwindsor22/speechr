#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 15:41:32 2018

@author: bradwindsor


import psycopg2


conn = psycopg2.connect(database = 'example', user='sys_speechr', password = 'pass' )
cur = conn.cursor()
cur.execute("CREATE TABLE Products(Id INTEGER PRIMARY KEY, Name VARCHAR(20), Price INT)")
cur.execute("INSERT INTO Products VALUES(1,'Milk',5)")
cur.execute("INSERT INTO Products VALUES(2,'Sugar',7)")
cur.execute("INSERT INTO Products VALUES(3,'Coffee',3)")
cur.execute("INSERT INTO Products VALUES(4,'Bread',5)")
cur.execute("INSERT INTO Products VALUES(5,'Oranges',3)")
conn.commit()

"""

import psycopg2 as pg
import sqlalchemy as sqa
import pandas as pd

#%%
engine = sqa.create_engine('postgresql://sys_speechr:pass@localhost:5432/example')


#%%
conn = pg.connect(database = 'example', user='sys_speechr', password = 'pass' )

df = pd.read_sql("SELECT * FROM Products", conn)

#%%
df.to_sql( 'products_2', engine, if_exists = 'replace', index=False)

#%%
df3 = pd.read_sql("SELECT * FROM products_2", engine)
