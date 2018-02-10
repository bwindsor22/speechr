# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 18:52:21 2018

@author: CSL
reference https://schedule.readthedocs.io/en/stable/api.html#main-interface
******************************************************************************
Important Notes:
Each time schedule.run_pending is executed, everey task that is planned using
the schedule.ever() is added to schedule.jobs.  Be sure to clear schedule.jobs
before you run to make sure duplicate jobs aren't running.

schedule.jobs = []
Default Jobs list

schedule.clear(tag=None)[source]
Calls clear on the default scheduler instance.

schedule.cancel_job(job)[source]
Calls cancel_job on the default scheduler instance.

schedule.next_run()[source]
Calls next_run on the default scheduler instance.
"""
import schedule
import time
import crawler
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

def run_jobs(logger):
    try:
        start_crawler(logger)
    except Exception as ex:
        logger.error('Job failed')
        logger.exception(ex)

def start_crawler(logger):
    logger.info('Starting job')
    c = crawler.Crawler()
    
    # define all the tasks you want to do
    def run_once():
        c.run()
        
    schedule.every(1).hour.do(run_once)
    schedule.run_all()
    
    
    while True:
        logger.info("Waiting. Next scheduled run start in local time: {}".format(schedule.next_run()))
        schedule.run_pending()
        time.sleep(10)
        
if __name__ == '__main__':
    logger = setup_logging()
    run_jobs(logger)
    