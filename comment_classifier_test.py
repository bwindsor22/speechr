#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 18:47:01 2018
"""
import unittest
import comment_classifier

class TestCommentClassifier(unittest.TestCase):
    def setUp(self):
        self.CC = comment_classifier.CommentClassifier(["Test_Slur_1", "Test_Slur_2"])
        
    
    def test_false_positives_are_zero(self):
        comments = [
            "This comment has no issues",
            "I hate bad apples in my food"
            ]

        self.assertEqual(0, self.CC.analyze(comments[0]))
        self.assertEqual(0, self.CC.analyze(comments[1]))

        
    def test_negatives(self):
        comments = [
            "Test_Slur_1", 
            "Test_Slur_1 Test_Slur_2",
            "hate disgusting bad negative words Test_Slur_1",
            ]
                
        self.assertLess(0, self.CC.analyze(comments[0]))
        self.assertLess(0, self.CC.analyze(comments[1]))
        self.assertLess(0, self.CC.analyze(comments[2]))

        #worse comments get worse scores
        self.assertLess(self.CC.analyze(comments[0]), self.CC.analyze(comments[2]))
        self.assertLess(self.CC.analyze(comments[0]), self.CC.analyze(comments[1]))


    def test_blank(self):
        comments = [
            ""
            ]
                
        self.assertEqual(0, self.CC.analyze(comments[0]))
        
    def test_lettercase(self):
        comments = [
            "TeSt_sLur_1",
            "test_slur_2"
            ]
                
        self.assertLess(0, self.CC.analyze(comments[0]))
        self.assertLess(0, self.CC.analyze(comments[1]))
        
        
if __name__ == '__main__':
    unittest.main()

