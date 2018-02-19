#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 00:14:03 2018

@author: bradwindsor
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 18:47:01 2018
"""
import unittest
import BagOfWordsClassifier

class TestBagOfWordsClassifier(unittest.TestCase):
    def setUp(self):
        self.BOWC = BagOfWordsClassifier.BagOfWordsClassifier()

    def test_false_positives_are_zero(self):
        comments = [
            "This comment has no issues",
            "I hate bad apples in my food"
            ]

        self.assertEqual(0, self.BOWC.analyze(comments[0]))
        self.assertEqual(0, self.BOWC.analyze(comments[1]))

        
    def test_negatives(self):
        comments = [
            "Test_Slur_1"
            ]
                
        self.assertEqual(5, self.BOWC.analyze(comments[0]))

    def test_blank(self):
        comments = [
            ""
            ]
                
        self.assertEqual(0, self.BOWC.analyze(comments[0]))
        
    def test_lettercase(self):
        comments = [
            "TeSt_sLur_1"
            ]
                
        self.assertEqual(5, self.BOWC.analyze(comments[0]))
        
        
if __name__ == '__main__':
    unittest.main()
