# -*- coding: utf-8 -*-
"""
LDA on verb infinitives
Created on Mon Apr 18 22:39:06 2011

@author: vene
"""
import numpy as np
import matplotlib.pyplot as pl
from scikits.learn.lda import LDA
from scikits.learn.svm import LinearSVC
from scikits.learn.metrics import classification_report
from preprocess import extract_features

target_names = ["covered", "no alternance", "uncovered"]
infinitives, y = [], []
with open('inf-ta-labeled.txt') as f:
    for line in f:
        inf, label = unicode(line).split()
        infinitives.append(inf)
        y.append(int(label))
        
infinitives, y = np.array(infinitives), np.array(y, dtype=np.float)

X, _ = extract_features(infinitives, 1, True)
clf = LinearSVC(multi_class=True).fit(X, y)
#model = LDA(n_components=2).fit(X, y)
y_pred = clf.predict(X)
print classification_report(y, y_pred, [0, 1, 2], target_names)
#Xtr = model.transform(X)
#pl.figure()
#for c, i, target_name in zip("rgb", [0, 1, 2], target_names):
#    pl.scatter(Xtr[y == i, 0], Xtr[y == i, 1], c=c, label=target_name)
#pl.legend()
#pl.title('LDA of infinitives')
#
#pl.show()
