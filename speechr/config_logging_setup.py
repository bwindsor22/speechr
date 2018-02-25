#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 10:17:22 2018
"""
import logging
import logging.config
import os
import json


def setup_logging():    
    app_path = os.path.dirname(os.path.abspath(__file__))
    logger_config = os.path.join(os.path.sep, app_path, 'config', 'logging_config') + '.json'
    if os.path.exists(logger_config):
        with open(logger_config, 'rt') as f:
            config = json.load(f)

    logging.config.dictConfig(config)
    
    logger = logging.getLogger("scheduler")
    return logger

def get_app_config():
    app_path = get_app_path()
    config_path = os.path.join(os.path.sep, app_path, 'config', 'app_config') + '.json'
    if os.path.exists(config_path):
        with open(config_path, 'rt') as f:
            config = json.load(f)
    return config

def get_app_path():
    return os.path.dirname(os.path.abspath(__file__))