import numpy as np
import sys

from sklearn.feature_extraction import DictVectorizer

from features import all_splits
from make_crfsuite_input import _build_feature_dict, syllabifications
from crf import StressCRF
from pystruct.learners import OneSlackSSVM, StructuredPerceptron

def word_to_feature_dict(word, stress, size=2, unigram=False):
    x = []
    y = []
    for left, right, label in all_splits(word):
        lsz = len(left)
        y.append(label)
        if unigram:
            # unigram features in window
            features = dict([(str(-1 - k), c) for k, c in enumerate(left[-size:])])
            features.update(dict([(str(1 + k), c) for k, c in enumerate(right[:size])]))
        else:
            features = {}
            for k in xrange(size):
                for i in xrange(size - k):
                    right_feature = right[i:i + k + 1]
                    left_feature = left[lsz - i - k - 1:lsz - i]
                    if len(right_feature) == k + 1:
                        features['%s-%s' % (i + 1, i + k + 1)] = right_feature
                    if len(left_feature) == k + 1:
                        features['%s-%s' % (-i - 1, -i - k - 1)] = left_feature
        x.append(features)
    word_stripped = word.replace('-', '')
    return (x, [_build_feature_dict(word_stripped, k, size, size)
               for k in xrange(len(word_stripped))],
        #(np.array(y) == 0).astype(int),
        np.array(y, dtype=int) + 2,
        np.array(stress, dtype=int))


if __name__ == '__main__':
    X_train, y_train = [], []
    vect_syl = DictVectorizer(sparse=True)
    vect_stress = DictVectorizer(sparse=True)
    vect_syl.feature_names_ = set()
    vect_stress.feature_names_ = set()
    # fit vectorizers
    for _, word, stress in syllabifications('../silabe.train.xml', 10):
        if len(word.strip().replace('-', '')) != len(stress):
            print >> sys.stderr, "Skipped %s" % word
            continue
        x_dict_syl, x_dict_stress, y_syl, y_stress = word_to_feature_dict(
                word.strip(), stress, size=4)
        for x in x_dict_syl:
            for f, v in x.iteritems():
                if isinstance(v, (str, unicode)):
                    f = "%s%s%s" % (f, vect_syl.separator, v)
                vect_syl.feature_names_.add(f)
        for x in x_dict_stress:
            for f, v in x.iteritems():
                if isinstance(v, (str, unicode)):
                    f = "%s%s%s" % (f, vect_stress.separator, v)
                vect_stress.feature_names_.add(f)
    vect_syl.feature_names_ = sorted(vect_syl.feature_names_)
    vect_syl.vocabulary_ = dict((f, i) for i, f in
                                enumerate(vect_syl.feature_names_))
    vect_stress.feature_names_ = sorted(vect_stress.feature_names_)
    vect_stress.vocabulary_ = dict((f, i) for i, f in
                                enumerate(vect_stress.feature_names_))

    print "Vectorizing..."
    for _, word, stress in syllabifications('../silabe.train.xml', 10):
        if len(word.strip().replace('-', '')) != len(stress):
            continue
        x_dict_syl, x_dict_stress, y_syl, y_stress = word_to_feature_dict(
                word.strip(), stress, size=4)
        if not len(x_dict_syl):
            print >> sys.stderr, "Empty features for %s" % word
            continue
        X_train.append((vect_syl.transform(x_dict_syl),
                        vect_stress.transform(x_dict_stress)))
        where_stress = y_stress.argmax()
        if y_stress[where_stress] == 1:
            y_stress[where_stress + 1:] = 2
        y_syl += 1
        y_train.append(np.r_[y_syl, y_stress])

    
    n_features = len(vect_syl.feature_names_) + len(vect_stress.feature_names_)
    n_states = np.max([k for y in y_train for k in y]) + 1
    from sklearn.utils import shuffle
    X_train, y_train = shuffle(X_train, y_train, random_state=0)
    print "Loading test data..."
    X_test, y_test = [], []
    for _, word, stress in syllabifications('../silabe.test.xml', 10):
        if len(word.strip().replace('-', '')) != len(stress):
            continue
        x_dict_syl, x_dict_stress, y_syl, y_stress = word_to_feature_dict(
                word.strip(), stress, size=4)
        if not len(x_dict_syl):
            print >> sys.stderr, "Empty features for %s" % word
            continue
        X_test.append((vect_syl.transform(x_dict_syl),
                       vect_stress.transform(x_dict_stress)))
        where_stress = y_stress.argmax()
        if y_stress[where_stress] == 1:
            y_stress[where_stress + 1:] = 2
        y_syl += 1
        y_test.append(np.r_[y_syl, y_stress])
