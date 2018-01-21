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
import time # keep for when we want to schedule program to run at a certain time
import crawler

# schedule.clear()

c = crawler.Crawler()

# define all the tasks you want to do
def tasks_to_run():
    c.run()
    
schedule.every(1).hour.do(tasks_to_run)

"""schedule.run_pending() checks which jobs are to be run and then runs the task
that is scheduled each time it is called.  The infinite loop basically keeps
allows the class to check keep checking when it needs to be run then runs it"""
while True:
    schedule.run_pending()
    time.sleep(20)
