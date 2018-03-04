#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 21:32:24 2018

"""
from multiprocessing import Process, Manager
import time

def f(d):
    d[1] += '1'
    d['2'] += 2
    time.sleep(2)
    print(d)

if __name__ == '__main__':
    manager = Manager()

    d = manager.dict()
    d[1] = '1'
    d['2'] = 2

    
    p1 = Process(target=f, args=(d,))
    p2 = Process(target=f, args=(d,))
    p1.start()
    p2.start()
    d[3]='3'
    p1.join()
    p2.join()

