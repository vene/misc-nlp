# -*- encoding: utf8 -*-

import fileinput
from StringIO import StringIO
from lxml import etree
import sys
import numpy as np


def get_stress(line):
    word = line.replace('-', '')
    source_chars, target_chars = u'á÷\u1ea5ä\u1eaféíďóöú', u'aââăăeiîoou'
    stress = [c in source_chars for c in word]
    pos = word.find(u'\u0301')
    if pos >= 0:
        word = word[:pos] + word[pos + 1:]
        stress[pos - 1] = True
        del stress[pos]
        pos = line.find(u'\u0301')
        line = line[:pos] + line[pos + 1:]
    table = dict((ord(s), t) for s, t in zip(source_chars, target_chars))
    table[769] = None  # appropriate encoding
    return line.translate(table), stress


def syllabifications(source='silabe.xml', limit=0):
    ctx = etree.iterparse(source, tag='form')
    for k, (_, elem) in enumerate(ctx):
        text, stress_tag = get_stress(unicode(elem.text).strip())
        assert len(stress_tag) == len(text.replace('-', ''))
        yield (unicode(elem.get('w')), text, stress_tag)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
        if limit and k == limit:
            break
    del ctx


def crfsuite_feature_names(size=4, negative=False):
    indices = range(-size, 0) if negative else range(1, size + 1)
    indices = map(str, indices)
    return '\t'.join(['c[%s]=%%s' % ''.join(indices[i:(i + k + 1)])
                      for k in range(size)
                      for i in range(size - k)])

def _build_feature_dict(s, position, size, ngram_size):
    features = {}
    l = len(s)
    for left in xrange(-size, size + 2):
        for sz in xrange(0, min(ngram_size, size - left + 1)):
            if position + left >= 0 and position + left + sz + 1 <= l:
                features['%s|%s' % (left, left + sz)] =\
                    s[position + left:position + left + sz + 1]
    return features


def _char_ngrams(s, size=4):
    s_len = len(s)
    ngrams = []
    for n in xrange(1, min(size + 1, s_len + 1)):
        for i in xrange(s_len - n + 1):
            ngrams.append(s[i: i + n])
    return ngrams

def get_split_features(word):
    k = 0
    before_split = []
    while k < (len(word) - 1):
        if word[k + 1] == '-':
            before_split.append(True)
            k += 2
        else:
            before_split.append(False)
            k += 1
    before_split.append(False)
    after_split = [False] + before_split[:-1]
    syll_from_left = np.cumsum(after_split)
    syll_from_right = np.cumsum(before_split[::-1])[::-1]
    fst = syll_from_left == 0
    snd = syll_from_left == 1
    lst = syll_from_right == 0
    pen = syll_from_right == 1
    return before_split, after_split, fst, snd, lst, pen


def crfsuite_features(word, stress, size, left_tpl, right_tpl):
    res = StringIO()    
    before, after, first, second, last, penultimate = get_split_features(word)
    word = word.replace('-', '')
    if not (len(stress) == len(word)):
        print >> sys.stderr, 'length mismatch'
        raise ValueError
    for (k, label, bf, af, fst, snd, lst, penult) in zip(xrange(len(word)), stress, before, after, first, second, last, penultimate):
#        print >> res, '%d\tbf=%d\taf=%d\tfst=%d\tsnd=%d\tlast=%d\tpenult=%d\t%s' % (
        print >> res, '%d\t%s' % (
            label,
#            bf,
#            af,
#            fst,
#            snd,
#            lst,
#            penult,
            '\t'.join("c[%s]=%s" % item
                      for item
                      in _build_feature_dict(word, k, 2, 2).items()))
    return res.getvalue()

if __name__ == '__main__':
    N = 2  # n-gram size
    left_tpl = [crfsuite_feature_names(k, True) for k in xrange(1, N + 1)]
    right_tpl = [crfsuite_feature_names(k, True) for k in xrange(1, N + 1)]

    for _, word, stress in syllabifications('../silabe.test.xml', 0):
        #fileinput.input(openhook=fileinput.hook_encoded("utf8")):
        try:
            print crfsuite_features(word.strip().lower(),
                                    stress,
                                    size=N,
                                    left_tpl=left_tpl,
                                    right_tpl=right_tpl)
        except ValueError:
            continue
