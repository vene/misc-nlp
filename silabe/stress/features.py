# -*- encoding: utf8 -*-

import codecs
import sys

from lxml import etree

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV


def strip_accents_leave_diacritics(line):
    source_chars, target_chars = u'á÷äéíďóöú', u'aâăeiîoou'
    table = dict((ord(s), t) for s, t in zip(source_chars, target_chars))
    table[769] = None  # appropriate encoding
    return line.translate(table)


def get_preprocessor(column, size, terminator=''):
    def preprocess(line):
        line = line[column]
        if column == 0:
            line = line[-size:] + terminator
        else:
            line = terminator + line[:size]
        return strip_accents_leave_diacritics(line)
    return preprocess


def all_splits(string_, separator='-'):
    last_sep = 0
    for k, char_ in enumerate(string_):
        if k == 0:
            continue
        elif string_[k - 1] == separator:
            last_sep = k
            continue
        else:
            if char_ == separator:
                last_sep = k
            left = string_[:k].replace(separator, '')
            right = string_[k:].replace(separator, '')
            yield (left, right, k - last_sep)


def syllabifications(source='silabe.xml', limit=0):
    ctx = etree.iterparse(source, tag='form')
    for k, (_, elem) in enumerate(ctx):
        yield (unicode(elem.get('w')),
               strip_accents_leave_diacritics(unicode(elem.text)))
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
        if limit and k == limit:
            break
    del ctx


def length_stats():
    char_lengths, syl_lengths = [], []
    for word, syl in syllabifications():
        char_lengths.append(len(word))
        syl_lengths.append(syl.count('-') + 1)
    return char_lengths, syl_lengths


def training_instances(source='silabe.train.xml'):
    for _, syl in syllabifications(source):
        for left, right, label in all_splits(syl.strip()):
            yield left, right, label


def rulebased_score(source='silabe.train.xml'):
    from rulebased import syll
    k = 0
    n = 0
    for word, syl in syllabifications(source):
        n += 1
        s1 = syll(u''.join(k for k in syl.strip() if k != '-'))
        if s1 == syl.strip():
            k += 1
        for _, _, label in all_splits(s1):
            yield label
    print k / float(n)

def shaped_instances(source='silabe.train.xml'):
    k = (((l, r), label) for (l, r, label) in training_instances(source))
    return map(list, zip(*k))


def stratified_train_test_split():
    from sklearn.cross_validation import StratifiedKFold
    print "Loading data..."
    instances = list(training_instances())
    y = [label for _, _, label in instances]

    print "Generating split..."
    train_indices, _ = iter(StratifiedKFold(y, k=2, indices=True)).next()
    del y
    train, test = [], []

    def assign((idx, instance)):
        if idx in train_indices:
            train.append(instance)
        else:
            test.append(instance)

    print "Splitting data..."
    map(assign, enumerate(instances))

    print "Writing to files..."
    with codecs.open('train.csv', 'w', encoding='utf8') as train_file:
        for instance in train:
            print >> train_file, "%s,%s,%d" % instance
    with codecs.open('test.csv', 'w', encoding='utf8') as test_file:
        for instance in test:
            print >> test_file, "%s,%s,%s" % instance


class ProjectionVectorizer(CountVectorizer):
    def __init__(self, column, binary=False, size=3, terminator='$'):
        self.column = column
        self.size = size
        self.terminator = terminator
        CountVectorizer.__init__(self,
                                 preprocessor=get_preprocessor(self.column,
                                                               self.size,
                                                               self.terminator),
                                 ngram_range=(1, size),
                                 analyzer='char',
                                 binary=binary)

    def set_params(self, **kwargs):
        CountVectorizer.set_params(self, **kwargs)
        CountVectorizer.__init__(self,
                                 preprocessor=get_preprocessor(self.column,
                                                               self.size,
                                                               self.terminator),
                                 ngram_range=(1, self.size),
                                 analyzer='char',
                                 binary=self.binary)


class HomogeneousFeatureUnion(FeatureUnion):
    def set_params(self, **params):
        for key, value in params.iteritems():
            for _, transf in self.transformer_list:
                transf.set_params(**{key: value})


def skl_features():
    from time import time
    vectorizer = HomogeneousFeatureUnion(
        [('left', ProjectionVectorizer(column=0)),
         ('right', ProjectionVectorizer(column=1))])
    pipe = Pipeline(
        [('vect', vectorizer),
         #('clf', LinearSVC())
         ('clf', SGDClassifier(n_jobs=4))
         ])
    grid = GridSearchCV(pipe, {
        'vect__size': range(1, 4 + 1),
        'vect__terminator': (u'$', u''),
        'clf__alpha': (1e-8, 1e-7, 1e-6, 1e-5, 1e-4)  # (0.00001, 0.0001, 0.001)
    }, cv=3, refit=True, verbose=2)
    print 'Loading data...'
    t0 = time()
    data, y = shaped_instances()
    print 'done in %2.2f' % (time() - t0)
    print 'Fitting...'
    t0 = time()
    grid.fit(data, y)
    print 'done in %2.2f' % (time() - t0)
    return grid


def crfsuite_feature_names(size=4, negative=False):
    indices = range(-size, 0) if negative else range(1, size + 1)
    indices = map(str, indices)
    return '\t'.join(['c[%s]=%%s' % ''.join(indices[i:(i + k + 1)])
                      for k in range(size)
                      for i in range(size - k)])


def crfsuite_features(source='silabe.train.xml', size=3, outfile=None):
    """Use sklearn vectorizers to build a crfsuite input file"""
    # build an appropriate file name
    if outfile is None:
        filename, _ = source.rsplit('.', 1)
        outfile = '.'.join((filename, 'crfsuite', str(size), 'txt'))
    left_tpl = [crfsuite_feature_names(k, True) for k in xrange(1, size + 1)]
    right_tpl = [crfsuite_feature_names(k, False) for k in xrange(1, size + 1)]
    left_analyzer = ProjectionVectorizer(column=0, size=size, terminator=''
                                         ).build_analyzer()

    right_analyzer = ProjectionVectorizer(column=1, size=size, terminator=''
                                          ).build_analyzer()

    outfile = codecs.open(outfile, 'w', encoding='utf8')
    for ii, (_, syl) in enumerate(syllabifications()):
        if ii % 50000 == 0:
            sys.stdout.write(str(ii / 50000))
            sys.stdout.flush()
        elif ii % 1000 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()

        for left, right, label in all_splits(syl.strip()):
            left = unicode(left)
            right = unicode(right)
            left_size = min(len(left), size)
            right_size = min(len(right), size)
            print >> outfile, '%d\t%s\t%s' % (
                label,
                left_tpl[left_size - 1] % tuple(left_analyzer((left, ''))),
                right_tpl[right_size - 1] % tuple(right_analyzer(('', right))))
        print >> outfile
    outfile.close()

if __name__ == '__main__':
    if sys.argv[1] == 'crfsuite':
        crfsuite_features('silabe.%s.xml' % sys.argv[2], int(sys.argv[3]))
    elif sys.argv[1] == 'sklearn':
        from sklearn.externals.joblib import dump
        print 'Training...'
        vectorizer = HomogeneousFeatureUnion(
            [('left', ProjectionVectorizer(column=0)),
             ('right', ProjectionVectorizer(column=1))]
        )
        vectorizer.set_params(terminator=u'$', size=4)
        pipe = Pipeline(
            [('vect', vectorizer),
             ('clf', SGDClassifier(n_jobs=4, alpha=1e-6))]
        )
        train_data, y_train = shaped_instances('silabe.train.xml')
        pipe.fit(train_data, y_train)
        #f = open('sgd_full_results_nb.txt', 'w')
        #print >> f, grid.grid_scores_, grid.best_params_, grid.best_score_
        #f.close()
        print 'Testing...'
        test_data, y_true = shaped_instances('silabe.test.xml')
        y_pred = pipe.predict(test_data)
        dump(y_pred, 'sgd_y_pred_nb')
