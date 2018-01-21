# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# print ("hello world!!!")
import schedule
import time

def job():
    print("chris")
    print(schedule.jobs)
    
schedule.every(4).seconds.do(job)

while True:
    # print("a")
    schedule.run_pending()
    # time.sleep(3)
    
    # print(schedule.next_run())
    
    

"""
test = schedule.Scheduler()
planned_job = test.every(1).second.do(job)

test.run_pending()
print(test.run_pending())"""
