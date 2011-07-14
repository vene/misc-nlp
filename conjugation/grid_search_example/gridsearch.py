# -*- coding: utf-8 -*-
"""
Grid search feature extraction and SVC parameters
on -ta infinitives. Useful example.

@author: vene
"""

from time import time
import numpy as np
import matplotlib.pyplot as pl
from scikits.learn.decomposition import RandomizedPCA
from scikits.learn.svm import LinearSVC
from scikits.learn.pipeline import Pipeline
from scikits.learn.grid_search import GridSearchCV
from scikits.learn.metrics import classification_report
from preprocess import InfinitivesExtractor, load_data

# Data attributes
targets = [0, 1, 2]
target_names = ["covered", "no alternance", "uncovered"]
target_colors = "rgb"
    
# Classification settings
pipeline = Pipeline([
    ('extr', InfinitivesExtractor()),
    ('svc', LinearSVC(multi_class=True))
])
parameters = {
    'extr__count': (True,False),
    'extr__n': (3, 4, 5, 6),
    'svc__C': (1e-1, 1e-2, 1e9)
}
grid_search = GridSearchCV(pipeline, parameters)

print "Loading data..."
X, y = load_data()
print "Searching for the best model..."
t0 = time()
grid_search.fit(X, y)
print "Done in %0.3f" % (time() - t0)
print "Best score: %0.3f" % grid_search.best_score
clf = grid_search.best_estimator
print clf
yp = clf.predict(X)
print classification_report(y, yp, targets, target_names)

#pl.figure()
#pl.title("Classification rate for 3-fold stratified CV")
#pl.xlabel("n-gram maximum size")
#pl.ylabel("successful classification rate")
#ns = range(1, 11)
#scores = [grid_search.grid_points_scores_[(('extr__n', i),)] for i in ns]
#pl.plot(ns, scores, 'o-')
#pl.show()

## Now we take apart the pipeline to do the plot
#X = clf.named_steps['extr'].transform(X)
#pca = RandomizedPCA(n_components=2).fit(X)
#Xpca = pca.transform(X)
#svc = clf.named_steps['svc']
#print classification_report(y, svc.predict(X), targets, target_names)
#h=.05
#x_min, x_max = Xpca[:,0].min()-1, Xpca[:,0].max()+1
#y_min, y_max = Xpca[:,1].min()-1, Xpca[:,1].max()+1
#xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
#                     np.arange(y_min, y_max, h))
#Z = svc.predict(pca.inverse_transform(np.c_[xx.ravel(), yy.ravel()]))
#Z = Z.reshape(xx.shape)
#pl.contourf(xx, yy, Z)
#pl.axis('off')
#pl.scatter(Xpca[:, 0], Xpca[:, 1], c=y)
#pl.show()