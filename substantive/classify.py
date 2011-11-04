import cPickle

import numpy as np

from sklearn.preprocessing import Binarizer
from sklearn.cross_validation import KFold
from sklearn.grid_search import GridSearchCV
from sklearn.svm.sparse import LinearSVC, SVC
from sklearn.metrics import classification_report

import preprocess

if __name__ == '__main__':
	X_sg, y_sg = preprocess.load_data('singular.txt')
	X_pl, y_pl = preprocess.load_data('plural.txt')

	X_sg_p, v_sg = preprocess.preprocess_data(X_sg, suffix='$', n=5,
											  return_vect=True, binarize=False)
	X_pl_p, v_pl = preprocess.preprocess_data(X_pl, suffix='$', n=5,
	                                          return_vect=True, binarize=False)

	try:
		pkl = open('svc_sg.pkl', 'r')
		print 'Stored singular model found, loading...'
		clf = cPickle.load(pkl)
		pkl.close()
	except IOError:
		clf = LinearSVC(C=0.1).fit(X_sg_p, y_sg)
		sg_model = open('svc_sg.pkl', 'wb')
		cPickle.dump(clf, sg_model)
		sg_model.close()

	print 'Loading neutral data...'
	X_sg_n_clean = preprocess.load_data('singular_n.txt', labels=False)
	X_sg_n = Binarizer(copy=False).transform(v_sg.transform(X_sg_n_clean))
	print 'Predicting...'
	y_sg_n = clf.predict(X_sg_n)
	print (y_sg_n == 0).mean()

	try:
		pkl = open('svc_pl.pkl', 'r')
		print 'Stored plural model found, loading...'
		clf = cPickle.load(pkl)
		pkl.close()
	except IOError:
		weights = [x.strip().endswith("uri") for x in X_pl]
		weights = 1 + np.array(weights, dtype=np.float)
		clf = LinearSVC(C=0.1)
		clf.fit(X_pl_p, y_pl)
		pl_model = open('svc_pl.pkl', 'wb')
		cPickle.dump(clf, pl_model)
		pl_model.close()
	print 'Loading neutral data...'
	X_pl_n_clean = preprocess.load_data('plural_n.txt', labels=False)
	X_pl_n = Binarizer(copy=False).transform(v_pl.transform(X_pl_n_clean))
	print 'Predicting...'
	y_pl_n = clf.predict(X_pl_n)
	print (y_pl_n == 1).mean()

	mf = np.logical_and((y_sg_n == 0), (y_pl_n == 1))
	fm = np.logical_and((y_sg_n == 1), (y_pl_n == 0))
	mm = np.logical_and((y_sg_n == 0), (y_pl_n == 0))
	ff = np.logical_and((y_sg_n == 1), (y_pl_n == 1))


	print ".\tf\tm\nm\t%d\t%d\nf\t%d\t%d" % (
		mf.sum(), mm.sum(), ff.sum(), fm.sum())

	print ".\tf\tm\nm\t%.4f\t%.4f\nf\t%.4f\t%.4f" % (
		mf.mean(), mm.mean(), ff.mean(), fm.mean())
	
	def print_word(i):
		print X_sg_n_clean[i].strip(), '/', X_pl_n_clean[i].strip()
	
	liniute_sg = liniute_pl = uri_pl_gresite = uri_pl_corecte = 0
	print "Words completely misclassified:"
	for i in np.flatnonzero(fm):
		print_word(i)
	print "\n\n\nWords with misclassified singular:"
	for i in np.flatnonzero(ff):
		if "-" in X_sg_n_clean[i]: 
			liniute_sg += 1
		print_word(i)
	print "\n\n\nWords with misclassified plural:"
	for i in np.flatnonzero(mm):
		if "-" in X_sg_n_clean[i]:
			liniute_pl += 1
		print_word(i)

	for i in np.flatnonzero(y_pl_n == 1):
		if X_pl_n_clean[i].strip()[-3:] == 'uri':
			uri_pl_corecte += 1
	for i in np.flatnonzero(y_pl_n == 0):
		if X_pl_n_clean[i].strip()[-3:] == 'uri':
			uri_pl_gresite += 1

	print "Dashes in misclassified sg: %d" % liniute_sg
	print "Dashes in misclassified pl: %d" % liniute_pl
	print "-uri plurals: correct %d, incorrect %d" % (uri_pl_corecte, uri_pl_gresite)
