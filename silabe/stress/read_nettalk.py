import sys
import numpy as np
from sklearn.feature_extraction import DictVectorizer

from load_data import word_to_feature_dict


def nettalk_syl_to_split(syl):
    syllables = [syl[k - 1] != '>' and syl[k] in ('>', '0', '1', '2')
                 for k in xrange(1, len(syl))]
    stress = [k == '1' for k in syl]
    return syllables, stress


def process_line(line):
    try:
        word, phon, syl, cls = line.strip().split('\t')
    except ValueError:
        return None, None, None, None
    #stress = nettalk_syl_to_split(syl)
    syllable, stress = nettalk_syl_to_split(syl)
    show_hyp = [{True: '-', False: ''}.get(tag) for tag in syllable] + ['']
    split_word = ''.join(ch for t in zip(word, show_hyp) for ch in t)
    return word, syllable, split_word, stress


def get_data(f='net/nettalk.data.txt', size=2):
    f = open(f)

    words = [process_line(line)[2:] for line in f]

    X, y = [], []
    vect_syl = DictVectorizer()
    vect_stress = DictVectorizer()
    vect_syl.feature_names_ = set()
    vect_stress.feature_names_ = set()
    for word, stress in words:
        if word is None:
            continue
        if len(word.strip().replace('-', '')) != len(stress):
            print >> sys.stderr, "Skipped %s" % word
            continue
        x_dict_syl, x_dict_stress, y_syl, y_stress = word_to_feature_dict(
            word.strip(), stress, size=size)
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

    for word, stress in words:
        if word is None:
            continue
        x_dict_syl, x_dict_stress, y_syl, y_stress = word_to_feature_dict(
            word, stress, size=size)
        if not len(x_dict_syl):
            print >> sys.stderr, "Empty features for {}".format(word)
            continue
        X.append((vect_syl.transform(x_dict_syl),
                  vect_stress.transform(x_dict_stress)))
        where_stress = y_stress.argmax()
        if y_stress[where_stress] == 1:
            y_stress[where_stress + 1:] = 2
        y_syl += 1
        y.append(np.r_[y_syl, y_stress])

    return X, y
