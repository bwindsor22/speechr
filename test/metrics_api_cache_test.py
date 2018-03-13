#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 14:57:35 2018

"""
from speechr import metrics_api_cache
from speechr import config_logging_setup
from speechr.endpoints_enum import Endpoints
import pytest

@pytest.fixture
def cache():
    config_logging_setup.setup_logging()
    cache = metrics_api_cache.Cache_Helper()
    return cache.refresh_cache()

def test_all_comments():
    assert 0 < len(cache()[Endpoints.all_comments])

def test_comment_rates():
    assert 0 < len(cache()[Endpoints.comment_rates])

