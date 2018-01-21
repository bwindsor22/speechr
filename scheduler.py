# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 18:52:21 2018

@author: CSL
"""

import schedule
import time
import crawler


# c = crawler.Crawler()
def test():
    print("chris")

schedule.every(1).minute.do(test)

for _ in range(0,999999):
    schedule.run_pending()
    time.sleep(3)
