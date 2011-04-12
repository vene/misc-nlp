# -*- coding: utf-8 -*-
"""
Runs some simple unsupervised visualisation tricks
on the corpus of romanian infinitives. For now, we
do PCA and NMF, with different settings.

Created on Tue Apr 12 19:02:07 2011

@author: vene
"""

import numpy as np
import matplotlib.pyplot as pl

from scikits.learn.feature_extraction import text
from scikits.learn.decomposition import RandomizedPCA, NMF
from scikits.learn.cluster import KMeans

class SimplePreprocessor(object):
    """Fast preprocessor suitable for roman languages"""

    # the space at the end = tiny hax for skl, will fix later
    def preprocess(self, unicode_text):
        return unicode(unicode_text.strip().lower() + self.suffix + " ")
        
    def __init__(self, suffix='$'):
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


def plot_projection(model, infinitives, title):
    fig = pl.figure()
    # Binary model: n-gram appears or not
    for i in range(1, 4):  # n-gram length (1 to 3)    
        pl.subplot(2, 3, i)
        data, _ = extract_features(infinitives, i, False)
        projected_data = model.fit(data).transform(data)
        pl.scatter(projected_data[:, 0], projected_data[:, 1])
        pl.title('Binary %d-grams' % i)
    # Frequency model: count the occurences
    for i in range(1, 4):
        pl.subplot(2, 3, 3 + i)
        data, _ = extract_features(infinitives, i, True)
        projected_data = model.fit(data).transform(data)
        pl.scatter(projected_data[:, 0], projected_data[:, 1])
        pl.title('Count %d-grams' % i)
    fig.text(.5, .95, title, horizontalalignment='center')
    pl.show()

def k_clusters(k, infinitives):
    data, _ = extract_features(infinitives, 2, True)
    kmeans = KMeans(k=k).fit(data)
    print kmeans.inertia_
    print kmeans.cluster_centers_


if __name__ == '__main__':
    with open('infinitives.txt') as f:
        infinitives = np.array([unicode(inf) for inf in f])
    ta = False
    if ta:   
        ends_in_ta = np.array([inf.endswith('ta\n') for inf in infinitives])
        infinitives = infinitives[ends_in_ta]
    
    plot_projection(RandomizedPCA(n_components=2), infinitives, 
                    "PCA projection of %s$ infinitives" % ("-ta" if ta else ""))
    plot_projection(NMF(n_components=2, tol=0.01, init="nndsvda"), infinitives, 
                    "NMF projection of %s$ infinitives" % ("-ta" if ta else ""))
    # k_clusters(3, infinitives)
#    print infinitives[0]
#    data, vect = extract_features(infinitives, 2, True)
#    print vect.vocabulary.keys()
#    for token, idx in vect.vocabulary.items():
#        if idx in data[0].nonzero()[0]:
#            print token
