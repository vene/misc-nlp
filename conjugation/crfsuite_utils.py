# -*- coding: utf-8 -*-

import sys
import codecs

from sklearn.feature_extraction.text import CountVectorizer


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


def crfsuite_feature_names(size=4, negative=False):
    indices = range(-size, 0) if negative else range(1, size + 1)
    indices = map(str, indices)
    return '\t'.join(['c[%s]=%%s' % ''.join(indices[i:(i + k + 1)])
                      for k in range(size)
                      for i in range(size - k)])


def crfsuite_features(source, size=3, outfile=None):
    """Use sklearn vectorizers to build a crfsuite input file.

    Parameters
    ----------

    source:
        sequence containing (left, right, label) or (left, this, right, label)

    TODO: factor the vectorizer out of this, assume already analyzed input?
    """
    # build an appropriate file name
    if outfile is None:
        outfile = '.'.join(('crfsuite', str(size), 'txt'))
    left_tpl = [crfsuite_feature_names(k, True) for k in xrange(1, size + 1)]
    right_tpl = [crfsuite_feature_names(k, False) for k in xrange(1, size + 1)]
    left_analyzer = ProjectionVectorizer(column=0, size=size, terminator=''
                                         ).build_analyzer()

    right_analyzer = ProjectionVectorizer(column=1, size=size, terminator=''
                                          ).build_analyzer()

    outfile = codecs.open(outfile, 'w', encoding='utf8')
    for ii, splits in enumerate(source):
        if ii % 50000 == 0:
            sys.stdout.write(str(ii / 50000))
            sys.stdout.flush()
        elif ii % 1000 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()

        for split in splits:
            this = None
            if len(split) == 4:
                left, this, right, label = split
            else:
                left, right, label = split
            left = unicode(left)
            this = unicode(this) if this is not None else None
            right = unicode(right)
            left_size = min(len(left), size)
            right_size = min(len(right), size)
            print >> outfile, ''.join((
                label,
                ('\t' + left_tpl[left_size - 1]
                    % tuple(left_analyzer((left, '')))
                    if left_size > 0 else ''),
                ('\tc[0]=%s\t' % this) if this is not None else '\t',
                (right_tpl[right_size - 1] % tuple(right_analyzer(('', right)))
                    if right_size > 0 else '')))
        print >> outfile
    outfile.close()
