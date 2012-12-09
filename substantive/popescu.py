# Approximately reproducing M. Popescu et al (see paper)
# They use a 3-class SVM with a string kernel, we use a linear
# SVM preceded by feature expansion for similar results

import numpy as np

from sklearn.svm import LinearSVC
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import StratifiedKFold, StratifiedShuffleSplit
import preprocess


if __name__ == '__main__':
    print 'Loading training and test data...'
    X_sg, y_sg = preprocess.load_data('data/singular.txt')
    X_sg_n_clean = preprocess.load_data('data/singular_n.txt', labels=False)
    X_sg = np.r_[X_sg, X_sg_n_clean]
    y_sg = np.r_[y_sg, 2 * np.ones(len(X_sg_n_clean))]
    X_sg_p = preprocess.preprocess_data(X_sg, suffix='$', n=5,
                                        return_vect=False, binarize=False)

    train_split, test_split = iter(StratifiedShuffleSplit(y_sg, 1,
                                   test_size=0.1, random_state=0)).next()

    X_train, y_train = X_sg[train_split], y_sg[train_split]
    X_test, y_test = X_sg[test_split], y_sg[train_split]
    raise Exception
    scores = np.empty((5, 2, 2))
    best_C = np.empty((5, 2, 2))
    vectorizers = np.empty((5, 2, 2), dtype=np.object)
    for i, n in enumerate((2, 3, 4, 5, 6)):
        for j, suffix in enumerate(('', '$')):
            for k, binarize in enumerate((True, False)):
                X_p, vect = preprocess.preprocess_data(X_train, suffix=suffix,
                                                       n=n, return_vect=True,
                                                       binarize=binarize)

                grid = GridSearchCV(LinearSVC(), n_jobs=-1,
                                    verbose=True,
                                    param_grid={'C': np.logspace(-2, 2, 5)},
                                    cv=StratifiedKFold(y_train, 10))

                grid.fit(X_p, y_train)
                scores[i, j, k] = grid.best_score_
                best_C[i, j, k] = grid.best_estimator_.C
                vectorizers[i, j, k] = vect


# We also applied our character n-gram feature extraction method in a similar
# way as (popescu cite) in order to give a clearer picture of the differences
# between the methods. Specifically, we took only the singulars and joined
# the masculine, feminine and neuters together to form a corpus of 30,308
# nouns. We procedeed to construct a stratified training and test split with
# ratio 9 to 1. We used stratified 10-fold cross-validation over the training
# set in order to choose the best model parameters from a grid, ultimately
# deciding on 6-grams with the dollar suffix and with binarization, while
# setting $C=0.01$. We then fit this classifier using the entire training set,
# and its behaviour on the held-out test set is given in table #REF#.
#
# Note that this is by no means a global optimum, 6 being the largest n-gram
# size within the parameter grid. But because this is not a main point of our
# study, and because the cross-validation scores are not too spread out (with
# a standard deviation of $0.012$) we do not expect such a method to be able
# to surpass the one we presented. In all fairness, we have tackled a different
# problem, using extra information (the plural forms), but we show that
# information to be crucial to such a model.
