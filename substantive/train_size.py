import cPickle
import numpy as np

from sklearn.preprocessing import Binarizer
from sklearn.utils import shuffle
from sklearn.svm import LinearSVC

from sklearn.externals.joblib import Parallel, delayed

import preprocess

def nouns_score(X, y, X_test, expected):
	clf = LinearSVC(C=0.1, scale_C=False)
	return np.mean(clf.fit(X, y).predict(X_test) == expected)


def sg_score(X, y, X_test): 
	return nouns_score(X, y, X_test, 0)


def pl_score(X, y, X_test): 
	return nouns_score(X, y, X_test, 1)


def plot(scores):
	import matplotlib.pylab as pl
	from matplotlib.ticker import FuncFormatter

	def percentages(x, pos=0):
		return '%2.2f%%'%(100*x)

	ax1 = pl.subplot(211)
	pl.errorbar(scores[:, 1], scores[:, 2], yerr=scores[:, 3],
				c='k', marker='o')
	pl.ylabel("Singular neuters as masculine")
	ax1.yaxis.set_major_formatter(FuncFormatter(percentages))
	ax2 = pl.subplot(212, sharex=ax1)
	pl.errorbar(scores[:, 1], scores[:, 4], yerr=scores[:, 5],
			    c='k', marker='o')

	pl.setp(ax2.get_xticklabels(), visible=False)
	pl.ylabel("Plural neuters as feminine")
	ax2.yaxis.set_major_formatter(FuncFormatter(percentages))
	pl.xlabel("Proportion of training set used")
	for ext in ('pdf', 'svg', 'png'):
		pl.savefig('train_size.%s' % ext)


if __name__ == '__main__':
	print 'Loading training and test data...'
	X_sg, y_sg = preprocess.load_data('singular.txt')
	X_pl, y_pl = preprocess.load_data('plural.txt')

	X_sg_p, v_sg = preprocess.preprocess_data(X_sg, suffix='$', n=5,
											  return_vect=True, binarize=False)
	X_pl_p, v_pl = preprocess.preprocess_data(X_pl, suffix='$', n=5,
	                                          return_vect=True, binarize=False)


	X_sg_n_clean = preprocess.load_data('singular_n.txt', labels=False)
	X_sg_n = Binarizer(copy=False).transform(v_sg.transform(X_sg_n_clean))

	X_pl_n_clean = preprocess.load_data('plural_n.txt', labels=False)
	X_pl_n = Binarizer(copy=False).transform(v_pl.transform(X_pl_n_clean))

	scores = []
	n_steps = 100
	for train_proportion in np.linspace(0.05, 1, 10):
		train_size = len(X_sg) * train_proportion
		print "Sampling %d nouns out of the training set..." % train_size

		X_sg_steps, y_sg_steps, X_pl_steps, y_pl_steps = zip(*[shuffle(
			X_sg_p, y_sg, X_pl_p, y_pl, n_samples=train_size)
			for k in xrange(n_steps)])
		print "Evaluating %d pairs of classifiers..." % n_steps
		sg_step_scores = Parallel(n_jobs=-1, verbose=False)(
			delayed(sg_score)(X_sg_step, y_sg_step, X_sg_n)
			for X_sg_step, y_sg_step in zip(X_sg_steps, y_sg_steps))
		pl_step_scores = Parallel(n_jobs=-1, verbose=False)(
			delayed(pl_score)(X_pl_step, y_pl_step, X_pl_n)
			for X_pl_step, y_pl_step in zip(X_pl_steps, y_pl_steps))
		score = (np.mean(sg_step_scores), np.std(sg_step_scores),
			     np.mean(pl_step_scores), np.std(pl_step_scores))
		print score
		scores.append((train_size, train_proportion) + score)
	print "Pickling scores..."
	scores = np.array(scores)
	np.save("train_size", scores)
