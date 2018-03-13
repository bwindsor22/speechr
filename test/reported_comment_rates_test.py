#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 23:30:26 2018
"""
from speechr import reported_comment_rates

import pytest

@pytest.fixture
def raw_table():
    CR = reported_comment_rates.Comment_Rates()
    return CR.get_raw_table()

