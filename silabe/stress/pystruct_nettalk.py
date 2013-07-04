from scipy.stats import expon

from read_nettalk import get_data
from crf import StressCRF
from perc import StructuredPerceptron
from pystruct.learners import OneSlackSSVM
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV
from sklearn.cross_validation import KFold, train_test_split
from crf import score

if __name__ == '__main__':
    for size in (2,):
        X, y = get_data(size=size)
        n_features = X[0][0].shape[1] + X[0][1].shape[1]
        n_states = max(k.max() for k in y) + 1
        X_tr, X_test, y_tr, y_test = train_test_split(X, y, test_size=0.5,
                                                      random_state=0)
        crf = StressCRF(n_states=n_states, n_features=n_features,
                        inference_method='ad3')
        pcps = [StructuredPerceptron(model=crf, verbose=2, max_iter=50)
                for _ in xrange(3)]
        for pcp, (train, test) in zip(pcps, KFold(len(X_tr), k=3,
                                                  random_state=0)):
            X_tr_, y_tr_, X_dev, y_dev = X_tr[train], y_tr[train], \
                                         X_tr[test], y_tr[test]
        pcp.fit(X_tr_, y_tr_, X_dev, y_dev)
        #print score(y_test, search.predict(X_test))

        svm = OneSlackSSVM(model=crf, verbose=2)
        search = RandomizedSearchCV(svm, {'C': expon(scale=100)},
                                    cv=KFold(len(X_tr), k=3),
                                    refit=True, n_iter=20)
        search.fit(X_tr, y_tr)
