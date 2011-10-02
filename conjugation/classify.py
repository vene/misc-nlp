import sys

import numpy as np

from sklearn.svm.sparse import SVC
from sklearn.linear_model.sparse import LogisticRegression
from preprocess import get_clf, load_data, preprocess_data
from sklearn.metrics import classification_report
from sklearn.cross_validation import LeaveOneOut, cross_val_score

if len(sys.argv) < 2:
    filename = 'inf-all-labeled.txt'
else:
    filename = sys.argv[1]

X, y = load_data(filename)
n = len(X)
X = preprocess_data(X, n=3, suffix='')

np.random.seed(42)
clf = clf=LogisticRegression(C=10)
print np.mean(cross_val_score(clf, X, y, cv=LeaveOneOut(n, indices=True)))
