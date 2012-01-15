"""Hand-made grid search to compute scores and hyperparameters"""


import sys

import numpy as np

from sklearn.svm.sparse import LinearSVC
from preprocess import get_clf, load_data, preprocess_data
from sklearn.metrics import classification_report
from sklearn.cross_validation import KFold, LeaveOneOut
from sklearn.grid_search import GridSearchCV

if __name__ == '__main__':
	filename = 'inf-all-labeled.txt'

	X, y = load_data(filename)
	n = len(X)
	scores = np.empty((5, 2, 2), dtype=np.float)
	best_C = np.empty((5, 2, 2), dtype=np.float)
	for i, ngrams in enumerate((2, 3, 4, 5, 6)):
		for j, suffix in enumerate(('', '$')):
			for k, binarize in enumerate((True, False)):
				print "ngrams=%d, suffix=%s, binarize=%s" % (ngrams, suffix, binarize)
				X_new = preprocess_data(X, n=ngrams, suffix=suffix, binarize=binarize)
				grid = GridSearchCV(estimator=LinearSVC(), n_jobs=4, verbose=False,
							    	param_grid={'C': (0.01, 0.03, 0.1, 0.3, 1, 1.3)},
									cv=LeaveOneOut(n, indices=True))
				grid.fit(X_new, y)
				scores[i, j, k] = grid.best_score
				best_C[i, j, k] = grid.best_estimator.C
