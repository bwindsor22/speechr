#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 14:57:35 2018

"""
from speechr import metrics_api_cache
from speechr import config_logging_setup

import pytest


@pytest.fixture
def cache():
    config_logging_setup.setup_logging()
    cache =  metrics_api_cache.Metrics_api_cache()
    return cache.setup_cache()

def test_all_comments():
    assert 0 < len(cache()['all_comments'])

def test_comment_rates():
    assert 0 < len(cache()['comment_rates'])
        