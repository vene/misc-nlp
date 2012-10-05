import numpy as np

from sklearn.utils import shuffle
from sklearn.svm import LinearSVC

from sklearn.externals.joblib import Parallel, delayed

import preprocess


def nouns_score(X_sg, y_sg, X_pl, y_pl, X_sg_test, X_pl_test):
    sg_clf = LinearSVC(C=0.1).fit(X_sg, y_sg)
    pl_clf = LinearSVC(C=0.1).fit(X_pl, y_pl)
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


def plot(scores, scores2=None):
    import matplotlib.pylab as pl
    from matplotlib.ticker import FuncFormatter

    def percentages(x, pos=0):
        return '%2.2f%%' % (100 * x)

    ax1 = pl.subplot(211)
    pl.errorbar(scores2[:, 1], scores2[:, 2], yerr=scores2[:, 5],
                c='k', marker='o')
    #if scores2 is not None:
    #    pl.errorbar(scores2[:, 1] + 0.02, scores2[:, 2], yerr=scores2[:, 5],
    #            c='0.5', marker='s')
    pl.ylabel("Singular acc.")
    ax1.yaxis.set_major_formatter(FuncFormatter(percentages))

    pl.xlabel("Proportion of training set used")
    ax2 = pl.subplot(212, sharex=ax1)
    pl.errorbar(scores[:, 1], scores[:, 3], yerr=scores[:, 6],
                c='k', marker='o')
    if scores2 is not None:
        pl.errorbar(scores2[:, 1], scores2[:, 3], yerr=scores2[:, 6],
                c='k', marker='s')

    ax2.yaxis.set_major_formatter(FuncFormatter(percentages))

    #ax3 = pl.subplot(313, sharex=ax2)
    pl.errorbar(scores[:, 1] + 0.02, scores[:, 4], yerr=scores[:, 7],
                c='0.5', marker='o')
    if scores2 is not None:
        pl.errorbar(scores2[:, 1] + 0.02, scores2[:, 4], yerr=scores2[:, 7],
                c='0.5', marker='s')
    pl.ylabel("Plural and combined acc.")
    #ax3.yaxis.set_major_formatter(FuncFormatter(percentages))
    #pl.setp(ax3.get_xticklabels(), visible=False)

    #pl.show()

    for ext in ('pdf', 'svg', 'png'):
        pl.savefig('train_size-i.%s' % ext)


if __name__ == '__main__':
    print 'Loading training and test data...'
    X_sg_all, y_sg_all = preprocess.load_data('singular.txt')
    X_pl_all, y_pl_all = preprocess.load_data('plural.txt')

    X_sg, y_sg, X_pl, y_pl = [], [], [], []
    for sg, this_y_sg, pl, this_y_pl in zip(X_sg_all, y_sg_all, X_pl_all,
                                            y_pl_all):
        # get rid of balauri
        sg = sg.strip()
        pl = pl.strip()
        if not (pl.endswith('uri') and sg.endswith('ur')):
            X_sg.append(sg)
            y_sg.append(this_y_sg)
            X_pl.append(pl)
            y_pl.append(this_y_pl)
    X_sg = np.array(X_sg)
    y_sg = np.array(y_sg)
    X_pl = np.array(X_pl)
    y_pl = np.array(y_pl)

    print len(X_sg)
    X_sg_p, v_sg = preprocess.preprocess_data(X_sg, suffix='$', n=5,
                                              return_vect=True, binarize=False)
    X_pl_p, v_pl = preprocess.preprocess_data(X_pl, suffix='$', n=5,
                                              return_vect=True, binarize=False)

    X_sg_n_clean = preprocess.load_data('singular_n.txt', labels=False)
    X_sg_n = v_sg.transform(X_sg_n_clean)
    #X_sg_n = Binarizer(copy=False).transform(v_sg.transform(X_sg_n_clean))

    X_pl_n_clean = preprocess.load_data('plural_n.txt', labels=False)
    X_pl_n = v_pl.transform(X_pl_n_clean)
    #X_pl_n = Binarizer(copy=False).transform(v_pl.transform(X_pl_n_clean))

    scores = []
    n_steps = 100
    print "size  \tratio\tsg_score\tpl_score\tscore   \tsg_std  \tpl_std  \tstd"
    for train_proportion in np.linspace(0.1, 1, 10):
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
        print "%d\t%.2f\t%.6f\t%.6f\t%.6f\t%.4e\t%.4e\t%.4e" % tuple(score)
        scores.append(score)
    print "Pickling scores..."

    scores = np.array(scores)
    plot(scores)
    np.save("train_size_i", scores)
