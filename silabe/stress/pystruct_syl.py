import numpy as np
import sys

from sklearn.feature_extraction import DictVectorizer

from features import all_splits
from make_crfsuite_input import _build_feature_dict, syllabifications
from crf import StressCRF
from pystruct.learners import StructuredPerceptron
from sklearn.grid_search import RandomizedSearchCV
from sklearn.cross_validation import ShuffleSplit
from crf import score

if __name__ == '__main__':
    crf = StressCRF(n_states=n_states, n_features=n_features,
                    inference_method='ad3')
    pcp = StructuredPerceptron(model=crf, max_iter=3, verbose=0, average=True)
    search = RandomizedSearchCV(pcp, {max_iter: range(50)},
                                n_iter=10, n_jobs=10, verbose=2, refit=True,
                                cv=ShuffleSplit(len(X_train), n_iter=1,
                                                test_size=0.25, random_state=0))
    search.fit(X_train, y_train)
    print score(y_test, search.predict(X_test))
