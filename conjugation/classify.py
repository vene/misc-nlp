import sys

import numpy as np

from sklearn.svm.sparse import SVC
from sklearn.linear_model.sparse import LogisticRegression
from preprocess import get_clf, load_data
from sklearn.metrics import classification_report
from sklearn.cross_val import StratifiedKFold

if len(sys.argv) < 2:
    filename = 'inf-all-labeled.txt'
else:
    filename = sys.argv[1]

X, y = load_data(filename)

np.random.seed(42)
train, test = iter(StratifiedKFold(y, 2)).next()
clf = get_clf(n=3, clf=LogisticRegression(C=10))
clf.fit(X[train], y[train])
print clf.score(X[test], y[test])
print classification_report(clf.predict(X[test]), y[test])
