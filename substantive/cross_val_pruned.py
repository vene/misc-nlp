import numpy as np

from sklearn.cross_validation import KFold
from sklearn.grid_search import GridSearchCV
from sklearn.svm.sparse import LinearSVC

import preprocess

if __name__ == '__main__':
    X_sg, y_sg = preprocess.load_data('data/singular.txt')
    X_pl, y_pl = preprocess.load_data('data/plural.txt')
    X_sg_n_all = preprocess.load_data('data/singular_n.txt', labels=False)
    X_pl_n_all = preprocess.load_data('data/plural_n.txt', labels=False)
    X_sg_n, X_pl_n = [], []
    for sg, pl in zip(X_sg_n_all, X_pl_n_all):
        sg = sg.strip()
        pl = pl.strip()
        if pl.endswith('i') and not pl.endswith('uri'):
            X_sg_n.append(sg)
            X_pl_n.append(pl)
    X_sg_n = np.array(X_sg_n)
    X_pl_n = np.array(X_pl_n)
    scores_sg = np.empty((5, 2, 2))
    predict_sg = np.empty((5, 2, 2))
    best_C_sg = np.empty((5, 2, 2))
    scores_pl = np.empty((5, 2, 2))
    best_C_pl = np.empty((5, 2, 2))
    predict_pl = np.empty((5, 2, 2))

    for i, n in enumerate((2, 3, 4, 5, 6)):
        for j, suffix in enumerate(('', '$')):
            for k, binarize in enumerate((True, False)):
                print "%d-%d-%d out of 411" % (i, j, k)
                X_sg_p, v_sg = preprocess.preprocess_data(X_sg, suffix=suffix,
                                                          n=n, return_vect=True,
                                                          binarize=binarize)
                X_pl_p, v_pl = preprocess.preprocess_data(X_pl, suffix=suffix,
                                                          n=n, return_vect=True,
                                                          binarize=binarize)

                grid1 = GridSearchCV(estimator=LinearSVC(), n_jobs=-1,
                                     verbose=True,
                                     param_grid={'C': np.logspace(-2, 2, 5)},
                                     cv=KFold(len(X_sg), k=10, indices=True))
                grid1.fit(X_sg_p, y_sg)
                scores_sg[i, j, k] = grid1.best_score
                best_C_sg = grid1.best_estimator.C
                clf = grid1.best_estimator

                X_sg_n_p = v_sg.transform(X_sg_n)
                y_sg_n = clf.predict(X_sg_n_p)
                predict_sg[i, j, k] = (y_sg_n == 0).mean()

                grid2 = GridSearchCV(estimator=LinearSVC(), n_jobs=-1,
                                     verbose=True,
                                     param_grid={'C': np.logspace(-2, 2, 5)},
                                     cv=KFold(len(X_pl), k=10, indices=True))
                grid2.fit(X_pl_p, y_pl)
                scores_pl[i, j, k] = grid2.best_score
                best_C_pl[i, j, k] = grid2.best_estimator.C
                clf = grid2.best_estimator

                X_pl_n_p = v_pl.transform(X_pl_n)
                y_pl_n = clf.predict(X_pl_n_p)
                predict_pl[i, j, k] = (y_pl_n == 1).mean()
    np.save("trained_models/scores_sg_i", scores_sg)
    np.save("trained_models/predict_sg_i", predict_sg)
    np.save("trained_models/best_C_sg_i", best_C_sg)
    np.save("trained_models/scores_pl_i", scores_pl)
    np.save("trained_models/predict_pl_i", predict_pl)
    np.save("trained_models/best_C_pl_i", best_C_pl)
