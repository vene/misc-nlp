import numpy as np
import sys

from sklearn.feature_extraction import DictVectorizer

from features import all_splits
from make_crfsuite_input import _build_feature_dict, syllabifications
from crf import StressCRF
from perc import StructuredPerceptron
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV
from sklearn.cross_validation import ShuffleSplit, train_test_split
from crf import score

if __name__ == '__main__':
    X_tr, X_dev, y_tr, y_dev = train_test_split(X_train, y_train, test_size=0.25, random_state=0) 
    crf = StressCRF(n_states=n_states, n_features=n_features,
                    inference_method='ad3')
    pcp = StructuredPerceptron(model=crf, verbose=2, max_iter=10)
   

    #search = GridSearchCV(pcp, [{'max_iter': [1], 'average': [True]},
    #                            {'max_iter': [5], 'average': [True, 4]},
    #                            {'max_iter': [10], 'average': [True, 5, 9]},
    #                            {'max_iter': [25], 'average': [True, 5, 24]}],
    #                      n_jobs=9, verbose=2, refit=True,
    #                      cv=ShuffleSplit(len(X_train), n_iter=1,
    #                                      test_size=0.25, random_state=0))
    pcp.fit(X_tr, y_tr, X_dev, y_dev)
    #print score(y_test, search.predict(X_test))
