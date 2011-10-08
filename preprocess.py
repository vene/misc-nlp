# -*- coding: utf-8 -*-
"""
Preprocessor and analyzer for infinitives
Created on Wed Apr 13 18:13:21 2011

@author: vene
"""

from scikits.learn.feature_extraction import text
import numpy as np

class SimplePreprocessor(object):
    """Fast preprocessor suitable for roman languages"""

    # the space at the end = tiny hax for skl, will fix later
    def preprocess(self, unicode_text):
        return unicode(unicode_text.strip().lower() + self.suffix + " ")
        
    def __init__(self, suffix=''):
        self.suffix = suffix


def extract_features(words, n, count=True):
    pp = SimplePreprocessor()
    analyzer = text.CharNGramAnalyzer(min_n=1, max_n=n, preprocessor=pp)
    vectorizer = text.CountVectorizer(analyzer=analyzer, max_df=None)
    
    transformed_words = vectorizer.fit_transform(words).toarray()
    transformed_words = np.array(transformed_words, dtype=np.float)
    if not count:
        transformed_words[transformed_words > 0] = 1.0
    return transformed_words, vectorizer
