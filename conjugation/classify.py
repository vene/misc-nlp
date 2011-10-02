import sys

import numpy as np

from sklearn.svm.sparse import SVC
from sklearn.linear_model.sparse import LogisticRegression
from preprocess import get_clf, load_data
from sklearn.metrics import classification_report
from sklearn.cross_validation import LeaveOneOut, cross_val_score

if len(sys.argv) < 2:
    filename = 'inf-all-labeled.txt'
else:
    filename = sys.argv[1]

X, y = load_data(filename)
n = len(X)

np.random.seed(42)
clf = get_clf(n=3, clf=LogisticRegression(C=10), suffix='')
print np.mean(cross_val_score(clf, X, y, cv=LeaveOneOut(n, indices=True)))
