#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 00:55:09 2018
"""

import itertools
import os
import csv

from speechr import config_logging_setup

def load_csv_resource_to_list(file_name):
    app_path = config_logging_setup.get_app_path()
    
    file_path = os.path.join(os.path.sep, app_path, 'ref', file_name) + '.csv'
    entries = []
    with open(file_path, 'r') as file:
        rdr = csv.reader(file)
        for row in rdr:
            entries.append(row)
    entries = list(itertools.chain.from_iterable(entries))
    return entries
