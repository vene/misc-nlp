# -*- coding: utf-8 -*-
"""
Preprocessor and analyzer for infinitives
Created on Wed Apr 13 18:13:21 2011

@author: vene
"""

from scikits.learn.feature_extraction.text import CharNGramAnalyzer, \
                                                  CountVectorizer
from scikits.learn.preprocessing import Binarizer
from scikits.learn.pipeline import Pipeline
from scikits.learn import naive_bayes

import numpy as np

class SimplePreprocessor(object):
    def preprocess(self, unicode_text):
        return unicode(unicode_text.strip().lower() + self.suffix)
        
    def __init__(self, suffix=''):
        self.suffix = suffix


def get_clf(n=3, binarize=True):
    steps = [('vectorizer', CountVectorizer(CharNGramAnalyzer(min_n=1, max_n=n,
                                          preprocessor=SimplePreprocessor())))]
    if binarize:
        steps.append(('binarizer', Binarizer(copy=False)))
        steps.append(('clf', naive_bayes.BernoulliNB()))
    else:
        steps.append(('clf', naive_bayes.MultinomialNB()))

    return Pipeline(steps)


def load_data(filename='inf-ta-labeled.txt'):
    infinitives, y = [], []
    with open(filename) as f:
        for line in f:
            inf, label = unicode(line).split()
            infinitives.append(inf)
            y.append(int(label))
    infinitives, y = np.array(infinitives), np.array(y, dtype=np.int)
    return infinitives, y