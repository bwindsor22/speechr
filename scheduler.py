# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 18:52:21 2018

@author: CSL
"""

import schedule
import time # keep for when we want to schedule program to run at a certain time
import crawler

# define all the tasks you want to do
def tasks_to_run():
    c = crawler.Crawler()
    c.run()

#Create a schedule.every() for every task you want to run.
schedule.every(1).hour.do(tasks_to_run)

# this actually executes the schedule class.
for _ in range(0,9999):
    schedule.run_pending()
    # time.sleep(2)
    
