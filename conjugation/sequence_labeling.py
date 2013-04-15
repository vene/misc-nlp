# -*- coding: utf-8 -*-
"""
Sequence labeling of verbs according to rules

Lists hand-made rules that cover almost all the data
and labels verbs according to the category they fit.

Created on Tue Mar 29 17:16:36 2011

@author: vene
"""

import sys
import re
import codecs
from time import time
from random import random

from crfsuite_utils import crfsuite_features

from sequence_rules import get_rules
rules = get_rules()

f = codecs.open("verbe-indprez.txt", 'r', encoding='utf-8-sig')

words = {}

print "Loading data in memory...",
for line in f:
    word, base, persoana = line.split()
    persoana = persoana.split(".")[3]
    if base in words:  # words.has_key(base):
        words[base].append((word, persoana))  # 3pl
    else:
        words[base] = [(word, persoana)]

print "done"


def build_instances(tagged):
    return [[(base[:k], base[k], base[k + 1:], tag[k]) for k in range(len(base))]
            for base, tag in tagged]


def check(forms, base, ruletags):
    root = None
    pers = set()
    rules, tags = ruletags
    for form, persoana in forms:
        match = re.match(rules[persoana], form)
        if match:
            if not root:
                root = match.groups()
            elif root != match.groups():
                continue
            pers.add(persoana)

    if len(pers) >= 6:
        repeat = False
        if tags[-1] in ['T8', 'T16'] and base[-2:] == 'ea':  # tag 2 letters
            repeat = True
        tagged_inf = []
        if len(root) > 1:
            tagged_inf += ['0'] * len(root[0]) + [tags[0]]
            root = root[1]
            tags = tags[1:]
        else:
            root = root[0]
        tagged_inf += ['0'] * len(root) + tags
        if repeat:
            tagged_inf.append(tags[-1])
        return tagged_inf
    else:
        return None

if __name__ == '__main__':
    proportion = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    labeled_train = []
    labeled_test = []
    seen_tags = set()
    unlabeled = []
    total_time = 0.0
    iter_percent = len(words) / 100
    iter_ten_percent = 10 * iter_percent
    for k, (base, forms) in enumerate(words.items()):
        if k % iter_ten_percent == 0:
            sys.stdout.write(str(k / iter_ten_percent))
            sys.stdout.flush()
        elif k % iter_percent == 0:
            sys.stdout.write('.')
            sys.stdout.flush()
        found = False
        t0 = time()
        for ruletags in rules:
            tagged_inf = check(forms, base, ruletags)
            if tagged_inf is not None:
                if len(base) != len(tagged_inf):
                    print base
                    print tagged_inf
                else:
                    if seen_tags.issuperset(tagged_inf):
                        # we have previously seen all of the tags here
                        if random() < proportion:
                            labeled_test.append((base, tagged_inf))
                        else:
                            labeled_train.append((base, tagged_inf))
                    else:
                        labeled_test.append((base, tagged_inf))
                    seen_tags.update(tagged_inf)
                    found = True
                total_time += time() - t0
                break
        if not found:
            unlabeled.append((base, [''] * len(base)))
    print '%f verbs per second.' % (total_time / len(words))
    print 'Generating crfsuite features...'
    for size in xrange(2, 9):
        crfsuite_features(build_instances(labeled_train), size=size,
                          outfile='crf.labeled.%s.train' % size)
        crfsuite_features(build_instances(labeled_test), size=size,
                          outfile='crf.labeled.%s.test' % size)
        crfsuite_features(build_instances(unlabeled), size=size,
                          outfile='crf.unlabeled.%s.txt' % size)
    seq_unlab = codecs.open('seq_unlabeled.txt', 'w', encoding='utf8')
    for base, _ in unlabeled:
        print >> seq_unlab, base
    seq_unlab.close()
