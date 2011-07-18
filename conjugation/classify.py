import sys

import numpy as np

from scikits.learn.svm.sparse import SVC
from scikits.learn.svm.libsvm import set_verbosity_wrap
from scikits.learn.linear_model.sparse import LogisticRegression
from preprocess import get_clf, load_data
from scikits.learn.metrics import classification_report
from scikits.learn.cross_val import StratifiedKFold
from scikits.learn.grid_search import GridSearchCV
if len(sys.argv) < 2:
    filename = 'inf-all-labeled.txt'
else:
    filename = sys.argv[1]

X, y = load_data(filename)

np.random.seed(42)
set_verbosity_wrap(1)
clf = get_clf(n=3, clf=SVC(kernel='linear'))
grid = GridSearchCV(clf, {'clf__C': np.logspace(-4, 10, num=15)},
                    cv=StratifiedKFold(y, k=2))
grid.fit(X, y)
print grid.best_score, grid.best_estimator
#for train, test in StratifiedKFold(y, 2):
#    clf = get_clf(n=3, clf=SVC())
#    clf.fit(X[train], y[train])
#    print clf.score(X[test], y[test])
 #print classification_report(clf.predict(X[test]), y[test])