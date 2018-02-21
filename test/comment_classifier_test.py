#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 18:47:01 2018
"""
import pytest
from speechr import comment_classifier

@pytest.fixture
def CC():
    return comment_classifier.CommentClassifier(["Test_Slur_1", "Test_Slur_2"], ["A"])

def test_subword_not_found():
    comments = ["test_slur_1_extension"]
    assert 0 == CC().analyze(comments[0])        

def test_false_positives_are_zero():
    comments = [
        "This comment has no issues",
        "I hate bad apples in my food"
        ]

    assert 0 == CC().analyze(comments[0])
    assert 0 == CC().analyze(comments[1])

    
def test_negatives():
    comments = [
        "Test_Slur_1", 
        "Test_Slur_1 Test_Slur_2",
        "hate disgusting bad negative words Test_Slur_1",
        ]
            
    assert 0 < CC().analyze(comments[0])
    assert 0 < CC().analyze(comments[1])
    assert 0 < CC().analyze(comments[2])

    #worse comments get worse scores
    assert CC().analyze(comments[0]) < CC().analyze(comments[2])
    assert CC().analyze(comments[0]) < CC().analyze(comments[1])

def test_violent_words():
    comments = ["Test_violent_word_1", "Test_violent_word_2", "kill, world peace Test_slur_1 slant eye"]
    #test to make sure that a comment still gets a negative score even if there is no negative words
    # self.assertLess(0,self.CC.analyze(comments[0])) # should be true
    # self.assertLess(0,self.CC.analyze(comments[1]))
    # self.assertLess(0,self.CC.analyze(comments[2])) # should still give a negative score despite the text
    
    assert CC().analyze("Test_slur_1") < CC().analyze(comments[2])

def test_blank():
    comments = [
        ""
        ]
            
    assert 0 == CC().analyze(comments[0])
    
def test_lettercase():
    comments = [
        "TeSt_sLur_1",
        "test_slur_2"
        ]
            
    assert 0 < CC().analyze(comments[0])
    assert 0 < CC().analyze(comments[1])
    

