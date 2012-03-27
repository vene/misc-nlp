import cPickle

import numpy as np

from sklearn.preprocessing import Binarizer
from sklearn.cross_validation import KFold
from sklearn.grid_search import GridSearchCV
from sklearn.svm.sparse import LinearSVC, SVC

import preprocess

if __name__ == '__main__':
    X_sg, y_sg = preprocess.load_data('singular.txt')
    X_pl, y_pl = preprocess.load_data('plural.txt')
    X_sg_n = preprocess.load_data('singular_n.txt', labels=False)
    X_pl_n = preprocess.load_data('plural_n.txt', labels=False)
    X_sg_p, v_sg = preprocess.preprocess_data(X_sg, suffix='$', n=5,
                                              return_vect=True, binarize=False)
    X_pl_p, v_pl = preprocess.preprocess_data(X_pl, suffix='$', n=5,
                                              return_vect=True, binarize=False)

    grid1 = GridSearchCV(estimator=SVC(kernel='linear'), n_jobs=4, verbose=True,
                         param_grid={'C': np.logspace(-5, 5, 11)},
                         cv=KFold(len(X_sg), k=10, indices=True))
    grid1.fit(X_sg_p, y_sg)
    print grid1.best_score
    print grid1.best_estimator.C

    grid2 = GridSearchCV(estimator=SVC(kernel='linear'), n_jobs=4, verbose=True,
                         param_grid={'C': np.logspace(-5, 5, 11)},
                         cv=KFold(len(X_pl), k=10, indices=True))
    grid2.fit(X_pl_p, y_pl)
    print grid2.best_score
    print grid2.best_estimator.C
