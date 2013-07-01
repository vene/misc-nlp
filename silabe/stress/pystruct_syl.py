import numpy as np

from sklearn.feature_extraction import DictVectorizer

from features import all_splits
from make_crfsuite_input import _build_feature_dict, syllabifications


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
    data_train = [word_to_feature_dict(word.strip(), stress, size=3)
                  for _, word, stress in syllabifications('../silabe.train.xml',
                                                          100)
                  if len(word.strip().replace('-', '')) == len(stress)]
    X_dict_train, X_dict_stress, y_train, y_stress = zip(*data_train)
    del data_train
    print "Vectorizing..."
    vect = DictVectorizer(sparse=True).fit([d for inst in X_dict_train
                                             for d in inst])
    X_train = [vect.transform(inst) for inst in X_dict_train]
    del X_dict_train
    n_features = len(vect.feature_names_)
    n_states = max(np.max([k for y in y_train for k in y]),
                   np.max([k for y in y_stress for k in y]))

    from sklearn.utils import shuffle
    X_train, y_train = shuffle(X_train, y_train, random_state=0)

    #pcp = StructuredPerceptron(model=crf, max_iter=50, verbose=1)
    #pcp.fit(X_train, y_train)
    #print pcp.score(X_train, y_train)
    #data_test = [word_to_feature_dict(word.strip())
    #             for _, word in syllabifications('silabe.test.xml', False)]
    #X_dict_test, y_test = zip(*data_test)
    #del data_test
    #X_test = [vect.transform(inst) for inst in X_dict_test]
    #del X_dict_test
    #y_test = [(inst == 0).astype(np.int) for inst in y_test]
    #print pcp.score(X_test, y_test)
    #y_pred = pcp.predict(X_test)
    #correct = 0
    #for true, pred in zip(y_test, y_pred):
    #    if (true == pred).all():
    #        correct += 1
    #print correct * 1.0 / len(y_test)
