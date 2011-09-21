import sys

import numpy as np

from sklearn.svm.sparse import SVC, LinearSVC
from sklearn.svm import LinearSVC as denseSVC
from sklearn.svm.libsvm import set_verbosity_wrap
from sklearn.linear_model.sparse import LogisticRegression
from preprocess import get_clf, load_data, preprocess_data
from sklearn.metrics import classification_report
from sklearn.cross_val import StratifiedKFold, cross_val_score, LeaveOneOut, _permutation_test_score
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model.sparse import SGDClassifier
if len(sys.argv) < 2:
    filename = 'inf-ta-labeled.txt'
else:
    filename = sys.argv[1]

X, y = load_data(filename)
n = len(X)
np.random.seed(42)
set_verbosity_wrap(1)
class_weights = {0: 4.51886792,
                 1: 36.84615385,
                 2: 95.8       ,
                 3: 119.75     ,
                 4: 95.8       ,
                 5: 119.75     ,
                 6: 1. 
                }
#clf = get_clf(n=3, clf=SVC(kernel='linear'))  # SVC(kernel='linear')
clf = SVC(C=0.1)
print "preprocessing..."
#X = preprocess_data(X)
# grid = GridSearchCV(clf, {'C': np.logspace(-1.5, -0.5, 5)}, # 'clf__C': np.logspace(-4, 10, num=15)
#                   cv=LeaveOneOut(n),
#                    )#fit_params={'class_weight': 'auto'})
# alpha=0.01 => scor 80.84% fara class weights
# 1e-5 0.777597402597 SVC
# 0.824675324675
print "running..."
b_scores = []
n_scores = []
for l in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
    print  "Step ", l
    for binarize in (True, False):
        rate = np.mean(cross_val_score(get_clf(l, binarize), X, y,
                       cv=LeaveOneOut(n, indices=True)))
        if binarize:
            b_scores.append(rate)
        else:
            n_scores.append(rate)

print b_scores
print n_scores

#y_test = []
#y_pred = []
#for train, test in LeaveOneOut(n, indices=True):    
#    y_test.append(y[test])
#    y_pred.append(clf.fit(X[train], y[train]).predict(X[test]))
#
#print classification_report(np.ravel(y_test), np.ravel(y_pred))
#grid.fit(X, y)
#print grid.best_score #, grid.best_estimator
#for train, test in StratifiedKFold(y, 2):
#    clf = get_clf(n=3, clf=SVC())
#    clf.fit(X[train], y[train])
#    print clf.score(X[test], y[test])
 #print classification_report(clf.predict(X[test]), y[test])
