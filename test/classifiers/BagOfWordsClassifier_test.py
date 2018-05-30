#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 18:47:01 2018
"""
import pytest
from speechr.classifiers import bow_classifier


@pytest.fixture
def BOWC():
    return bow_classifier.BagOfWordsClassifier()

def test_false_positives_are_zero():
    comments = [
        "This comment has no issues",
        "I hate bad apples in my food"
        ]

    assert 0 == BOWC().analyze(comments[0])
    assert 0 == BOWC().analyze(comments[1])

    
def test_negatives():
    comments = [
        "Test_Slur_1"
        ]
            
    assert 5 == BOWC().analyze(comments[0])

def test_blank():
    comments = [
        ""
        ]
            
    assert 0 == BOWC().analyze(comments[0])
    
def test_lettercase():
    comments = [
        "TeSt_sLur_1"
        ]
            
    assert 5 == BOWC().analyze(comments[0])
    
        
