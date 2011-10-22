import sys

import numpy as np

from sklearn.svm.sparse import LinearSVC
# from sklearn.linear_model.sparse import LogisticRegression
from preprocess import get_clf, load_data, preprocess_data
from sklearn.metrics import classification_report
from sklearn.cross_validation import KFold, cross_val_score

if __name__ == '__main__':
	if len(sys.argv) < 2:
	    filename = 'inf-all-labeled.txt'
	else:
	    filename = sys.argv[1]

	X, y = load_data(filename)
	n = len(X)
	for ngrams in (1, 2, 3, 4, 5, 6):
		for suffix in ('', '$'):
			for binarize in (True, False):
				X_new = preprocess_data(X, n=ngrams, suffix=suffix, binarize=binarize)
				for C in (0.01, 0.03, 0.1, 0.3, 1, 1.3):
					clf = LinearSVC(C=C)
					print "n=%d s=%s b=%s C=%.2f: " % (ngrams, suffix, binarize, C),
					print np.mean(cross_val_score(clf, X_new, y, cv=KFold(n, 10, indices=True),
								  verbose=False, n_jobs=4))
