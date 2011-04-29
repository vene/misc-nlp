# -*- coding: utf-8 -*-
"""
Preprocessor and analyzer for infinitives
Created on Wed Apr 13 18:13:21 2011

@author: vene
"""

from scikits.learn.feature_extraction.text import CharNGramAnalyzer, \
                                                  CountVectorizer
import numpy as np

class SimplePreprocessor(object):
    def preprocess(self, unicode_text):
        return unicode(unicode_text.strip().lower() + self.suffix)
        
    def __init__(self, suffix=''):
        self.suffix = suffix

class InfinitivesExtractor(CountVectorizer):
    def __init__(self, n=1, count=True):
        self.n = n
        self.count=count
        analyzer = CharNGramAnalyzer(min_n=1, max_n=self.n,
                                          preprocessor=SimplePreprocessor())
        CountVectorizer.__init__(self, analyzer=analyzer, max_df=None)
        
    def _postprocess(self, X):
        """Adapts the format to my needs"""
        X = np.array(X, dtype=np.float)
        if not self.count:
            X[X > 0] = 1.0
        return X
        
    def fit_transform(self, X, y=None):
        if self.analyzer.max_n != self.n:
            self.analyzer = CharNGramAnalyzer(min_n=1, max_n=self.n,
                                              preprocessor=SimplePreprocessor())
        transformed_words = CountVectorizer.fit_transform(self, X).toarray()
        return self._postprocess(transformed_words)
        
    def fit(self, X, y=None):
        self.fit_transform(X, y)
        return self
        
    def transform(self, X):
        transformed = CountVectorizer.transform(self, X).toarray()
        return self._postprocess(transformed)
