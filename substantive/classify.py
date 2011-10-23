import cPickle

import numpy as np

from sklearn.preprocessing import Binarizer
from sklearn.cross_validation import KFold
from sklearn.grid_search import GridSearchCV
from sklearn.svm.sparse import LinearSVC

import preprocess

if __name__ == '__main__':
	X_sg, y_sg = preprocess.load_data('singular.txt')
	X_pl, y_pl = preprocess.load_data('plural.txt')

	X_sg_p, v_sg = preprocess.preprocess_data(X_sg, suffix='$', n=2,
											  return_vect=True)
	X_pl_p, v_pl = preprocess.preprocess_data(X_pl, suffix='$', n=2,
	                                          return_vect=True)

	try:
		pkl = open('svc_sg.pkl', 'r')
		print 'Stored singular model found, loading...'
		clf = cPickle.load(pkl)
		pkl.close()
	except IOError:
		grid1 = GridSearchCV(estimator=LinearSVC(), n_jobs=2, verbose=True,
						     param_grid={'C': np.logspace(-3, 3, 7)},
							 cv=KFold(len(X_sg), k=10, indices=True))
		grid1.fit(X_sg_p, y_sg)
		print grid1.best_score
		print grid1.best_estimator.C
		sg_model = open('svc_sg.pkl', 'wb')
		cPickle.dump(grid1.best_estimator, sg_model)
		clf = grid1.best_estimator
		sg_model.close()

	print 'Loading neutral data...'
	X_sg_n = preprocess.load_data('singular_n.txt', labels=False)
	X_sg_n = Binarizer(copy=False).transform(v_sg.transform(X_sg_n))
	print 'Predicting...'
	y_sg_n = clf.predict(X_sg_n)
	print (y_sg_n == 0).mean()

	try:
		pkl = open('svc_pl.pkl', 'r')
		print 'Stored plural model found, loading...'
		clf = cPickle.load(pkl)
		pkl.close()
	except IOError:
		grid2 = GridSearchCV(estimator=LinearSVC(), n_jobs=2, verbose=True,
					    	 param_grid={'C': np.logspace(-3, 3, 7)},
							 cv=KFold(len(X_pl), k=10, indices=True))
		grid2.fit(X_pl_p, y_pl)
		print grid2.best_score
		print grid2.best_estimator.C
		pl_model = open('svc_pl.pkl', 'wb')
		cPickle.dump(grid2.best_estimator, pl_model)
		clf = grid2.best_estimator
		pl_model.close()
	print 'Loading neutral data...'
	X_pl_n = preprocess.load_data('plural_n.txt', labels=False)
	X_pl_n = Binarizer(copy=False).transform(v_pl.transform(X_pl_n))
	print 'Predicting...'
	y_pl_n = clf.predict(X_pl_n)
	print (y_pl_n == 1).mean()
