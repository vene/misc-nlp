# -*- encoding: utf8 -*-

from lxml import etree
import codecs
import random

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion


def all_splits(string_, separator='-'):
    for k, char_ in enumerate(string_):
        if k == 0:
            continue
        elif string_[k - 1] == separator:
            continue
        else:
            left = string_[:k].replace(separator, '')
            right = string_[k:].replace(separator, '')
            yield (left, right, char_ == separator)


def syllabifications(source='silabe.xml', subsample=1):
    if subsample < 1:
        random.seed(0)
    ctx = etree.iterparse(source, tag='form')
    for k, (_, elem) in enumerate(ctx):
        if subsample < 1 and random.random() > subsample:
            continue
        yield elem.get('w'), elem.text
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
        #if k == 10:
        #    break
    del ctx


def length_stats():
    char_lengths, syl_lengths = [], []
    for word, syl in syllabifications():
        char_lengths.append(len(word))
        syl_lengths.append(syl.count('-') + 1)
    return char_lengths, syl_lengths


def training_instances():
    for _, syl in syllabifications():
        for left, right, label in all_splits(syl.strip()):
            yield unicode(left), unicode(right), label


def get_preprocessor(column, size, terminator):
    def strip_accents_leave_diacritics(line):
        line = line[column]
        if column == 0:
            line = line[-size:] + terminator
        else:
            line = terminator + line[:size]
        source_chars, target_chars = u'á÷äéíďóöú', u'aâăeiîoou'
        table = dict((ord(s), t) for s, t in zip(source_chars, target_chars))
        return line.translate(table)
    return strip_accents_leave_diacritics


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
        CountVectorizer.__init__(self,
                                 preprocessor=get_preprocessor(column, size,
                                                               terminator),
                                 ngram_range=(1, size),
                                 analyzer='char',
                                 binary=binary)

#    def fit_transform(self, documents):
#        return CountVectorizer.fit_transform(self,
#                                             ifilter(lambda x: x[self.column],
#                                                     documents))


def skl_features():
    from time import time
    vectorizer = FeatureUnion([('left', ProjectionVectorizer(column=0)),
                               ('right', ProjectionVectorizer(column=1))])
    print 'Loading data...'
    t0 = time()
    data = list(training_instances())
    print 'done in %2.2f' % (time() - t0)
    print 'Fitting...'
    t0 = time()
    vectorizer.fit(data)
    print 'done in %2.2f' % (time() - t0)
    print 'Transforming...'
    return vectorizer.transform(data)
    print 'done in %2.2f' % (time() - t0)


def crfsuite_feature_names(size=3, negative=False):
    indices = range(-size, 0) if negative else range(1, size + 1)
    indices = map(str, indices)
    return '\t'.join(['c[%s]=%%s' % ''.join(indices[i:(i + k + 1)])
                    for k in range(size)
                    for i in range(size - k)])


def crfsuite_features(size=3):
    left_tpl = [crfsuite_feature_names(k, True) for k in xrange(1, size + 1)]
    right_tpl = [crfsuite_feature_names(k, False) for k in xrange(1, size + 1)]
    left_analyzer = ProjectionVectorizer(column=0, size=size, terminator=''
                                         ).build_analyzer()

    right_analyzer = ProjectionVectorizer(column=1, size=size, terminator=''
                                          ).build_analyzer()

    outfile = codecs.open('crfsuite.all.%d.txt' % size, 'w', encoding='utf8')
    for _, syl in syllabifications():
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
#    outfile = codecs.open('svm_text.csv', 'w', encoding='utf8')
#    for left, right, label in training_instances():
#        print >> outfile, '%s,%s,%d' % (left, right, label)
    crfsuite_features()
