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
from multiprocessing import Process

from speechr import config_logging_setup
from speechr import metrics_api_cache
from speechr import flask_app

def run_jobs(logger):
    try:
        start_crawler(logger)
    except Exception as ex:
        logger.error('Job failed')
        logger.exception(ex)

def start_flask_and_cache():
    cache_maker = metrics_api_cache.Metrics_api_cache()
    cache = cache_maker.refresh_cache()
    thread = Process(target=run_flask, args=(cache,))
    thread.start()
    return cache_maker

def run_flask(cache):
    flask_app.FlaskApp(cache)
    

def start_crawler(logger):
    logger.info('Starting job')
    c = crawler.Crawler()
    cache_maker = start_flask_and_cache()

    # define all the tasks you want to do
    def run_once():
        c.run()
        cache_maker.refresh_cache()
    
    
    schedule.every(1).hour.do(run_once)
    schedule.run_all()

    
    while True:
        logger.info("Waiting. Next scheduled run start in local time: {}".format(schedule.next_run()))
        schedule.run_pending()
        time.sleep(10)
        
if __name__ == '__main__':
    logger = config_logging_setup.setup_logging()
    run_jobs(logger)
    