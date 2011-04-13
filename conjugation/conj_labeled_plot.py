# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 18:15:06 2011

@author: vene
"""
import gc
import numpy as np
import matplotlib.pyplot as pl
from preprocess import extract_features
from scikits.learn.decomposition import RandomizedPCA, NMF


models = {'PCA': RandomizedPCA(n_components=2, copy=False),
          'NMF': NMF(n_components=2, init='nndsvda')}
max_n = 3
suffix_length = 3  # 0 for whole words 
colors = 'ryb'
legend_titles = ["covered", "no alternance", "uncovered"]
infinitives, labels = [], []
with open('inf-ta-labeled.txt') as f:
    for line in f:
        inf, label = unicode(line).split()
        infinitives.append(inf[-suffix_length:])
        labels.append(int(label))
        
infinitives, labels = np.array(infinitives), np.array(labels)

for model_name, model in models.items():
    fig = pl.figure()
    for count, count_title in zip((False, True), ("Binary", "Frequency")):
        for i in xrange(1, max_n + 1):
            gc.collect()
            pl.subplot(2, max_n, (max_n if count else 0) + i)
            X, _ = extract_features(infinitives, i, count) 
            proj = model.fit(X).transform(X)
            for y, c, lgnd in zip(xrange(3), colors, legend_titles):
                view = proj[labels == y]
                pl.scatter(view[:, 0], view[:, 1], c=c, label=lgnd)
            pl.title("%s %d-grams" % (count_title, i))
    title = "%s projection of labeled -ta verbs" % model_name
    if suffix_length:
        title += " as %d-suffixes" % suffix_length
    fig.text(.5, .95, title,
             horizontalalignment='center')
    pl.show()