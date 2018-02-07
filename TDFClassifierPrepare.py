#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 22:10:36 2018
Modified from 
https://github.com/t-davidson/hate-speech-and-offensive-language
"""

import pandas as pd
import numpy as np

df = pd.read_csv("../data/labeled_data.csv")

df.columns = df.columns.str.strip()

tweets = df.tweet

