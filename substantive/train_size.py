import numpy as np

from sklearn.preprocessing import Binarizer
from sklearn.utils import shuffle
from sklearn.svm import LinearSVC

from sklearn.externals.joblib import Parallel, delayed

import preprocess


def nouns_score(X_sg, y_sg, X_pl, y_pl, X_sg_test, X_pl_test):
    sg_clf = LinearSVC(C=0.1, scale_C=False).fit(X_sg, y_sg)
    pl_clf = LinearSVC(C=0.1, scale_C=False).fit(X_pl, y_pl)
    sg_pred = sg_clf.predict(X_sg_test)
    pl_pred = pl_clf.predict(X_pl_test)
    sg_score = np.mean(sg_pred == 0)
    pl_score = np.mean(pl_pred == 1)
    overall_score = np.mean(np.logical_and(sg_pred == 0, pl_pred == 1))
    return sg_score, pl_score, overall_score


def sg_score(X, y, X_test):
    return nouns_score(X, y, X_test, 0)


def pl_score(X, y, X_test):
    return nouns_score(X, y, X_test, 1)


def plot(scores):
    import matplotlib.pylab as pl
    from matplotlib.ticker import FuncFormatter

    def percentages(x, pos=0):
        return '%2.2f%%' % (100 * x)

    ax1 = pl.subplot(311)
    pl.errorbar(scores[:, 1], scores[:, 2], yerr=scores[:, 5],
                c='k', marker='o')
    pl.ylabel("Singular accuracy")
    ax1.yaxis.set_major_formatter(FuncFormatter(percentages))

    ax2 = pl.subplot(312, sharex=ax1)
    pl.errorbar(scores[:, 1], scores[:, 3], yerr=scores[:, 6],
                c='k', marker='o')

    pl.ylabel("Plural accuracy")
    ax2.yaxis.set_major_formatter(FuncFormatter(percentages))

    ax3 = pl.subplot(313, sharex=ax2)
    pl.errorbar(scores[:, 1], scores[:, 4], yerr=scores[:, 7],
                c='k', marker='o')
    pl.ylabel("Overall accuracy")
    ax3.yaxis.set_major_formatter(FuncFormatter(percentages))
    pl.setp(ax3.get_xticklabels(), visible=False)
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
    print "size  P\tratio\tsg_err\tpl_err\terror \tsg_std  \tpl_std  \tstd"
    for train_proportion in np.linspace(0.05, 1, 10):
        train_size = len(X_sg) * train_proportion
        steps = [shuffle(X_sg_p, y_sg, X_pl_p, y_pl, n_samples=train_size)
                 for k in xrange(n_steps)]
        step_scores = Parallel(n_jobs=-1, verbose=False)(
            delayed(nouns_score)(*step, X_sg_test=X_sg_n, X_pl_test=X_pl_n)
            for step in steps)
        step_scores = np.array(step_scores)

        score = np.r_[train_size, train_proportion,
                      step_scores.mean(axis=0),
                      step_scores.std(axis=0)]
        print "%d\t%.2f\t%.4f\t%.4f\t%.4f\t%.2e\t%.2e\t%.2e" % tuple(score)
        scores.append(score)
    print "Pickling scores..."

    scores = np.array(scores)
    np.save("train_size", scores)
