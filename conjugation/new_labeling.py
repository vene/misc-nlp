# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 17:16:36 2011

@author: vene
"""

from __future__ import division
import re
import codecs

import numpy as np

f = codecs.open('verbe-indprez.txt', 'r', encoding='utf-8-sig')
#g = codecs.open('inf-doar-ez.txt', 'w', encoding='utf-8')
labeled = codecs.open('inf-all-labeled.txt', 'w', encoding='utf-8')
#h = codecs.open('inf-doar-esc.txt', 'w', encoding='utf-8')
#esclabeled = codecs.open('inf-esc-labeled.txt', 'w', encoding='utf-8')
rules = []

rules.append({'1sg': u'^([a-zăâîşţ]+)ez$',
         '2sg': u'^([a-zăâîşţ]+)ezi$',
         '3sg': u'^([a-zăâîşţ]+)ază$',
         '1pl': u'^([a-zăâîşţ]+)em$',
         '2pl': u'^([a-zăâîşţ]+)aţi$',
         '3pl': u'^([a-zăâîşţ]+)ază$'})

rules.append({'1sg': u'^([a-zăâîşţ]+)ez$',
         '2sg': u'^([a-zăâîşţ]+)ezi$',
         '3sg': u'^([a-zăâîşţ]+)ează$',
         '1pl': u'^([a-zăâîşţ]+)ăm$',
         '2pl': u'^([a-zăâîşţ]+)aţi$',
         '3pl': u'^([a-zăâîşţ]+)ează$'})

rules.append({'1sg': u'^([a-zăâîşţ]+)esc$',
         '2sg': u'^([a-zăâîşţ]+)eşti$',
         '3sg': u'^([a-zăâîşţ]+)eşte$',
         '1pl': u'^([a-zăâîşţ]+)im$',
         '2pl': u'^([a-zăâîşţ]+)iţi$',
         '3pl': u'^([a-zăâîşţ]+)esc$'})

rules.append({'1sg': u'^([a-zăâîşţ]+)sc$',
         '2sg': u'^([a-zăâîşţ]+)şti$',
         '3sg': u'^([a-zăâîşţ]+)şte$',
         '1pl': u'^([a-zăâîşţ]+)ştem$',
         '2pl': u'^([a-zăâîşţ]+)şteţi$',
         '3pl': u'^([a-zăâîşţ]+)sc$'})

rules.append({'1sg': u'^([a-zăâîşţ]+)$',
         '2sg': u'^([a-zăâîşţ]+)i$',
         '3sg': u'^([a-zăâîşţ]+)e$',
         '1pl': u'^([a-zăâîşţ]+)em$',
         '2pl': u'^([a-zăâîşţ]+)eţi$',
         '3pl': u'^([a-zăâîşţ]+)$'})

rules.append({'1sg': u'^([a-zăâîşţ]+)n$',
         '2sg': u'^([a-zăâîşţ]+)i$',
         '3sg': u'^([a-zăâîşţ]+)ne$',
         '1pl': u'^([a-zăâîşţ]+)nem$',
         '2pl': u'^([a-zăâîşţ]+)neţi$',
         '3pl': u'^([a-zăâîşţ]+)n$'})

words = {}

for line in f:
    word, base, persoana = line.split()
    persoana = persoana.split(".")[3]
    if words.has_key(base):
        words[base].append((word, persoana))  # 3pl
    else:
        words[base] = [(word, persoana)]

def check(forms, rules):
    root = None
    pers = set()
    for form, persoana in forms:
        match = re.match(rules[persoana], form)
        if match:
            if not root:
                root = match.groups()[0]
            elif root != match.groups()[0]:
                continue
            pers.add(persoana)

    return len(pers) >= 6


count = np.zeros(len(rules))
for base, forms in words.items():
    label_ez = 0
    label_esc = 0
    flags, = np.where([check(forms, rls) for rls in rules])
    
    matches = len(flags)
    if matches > 1:
        print base, flags
    if matches == 0:
        label = 0
    else:
        label = 1 + flags[0]  # index of the first match 

    count[flags] += 1

    print >> labeled, u"%s\t%d" % (base, label)

print "Captured: ", count
print "out of %d" % len(words)
for fl in (f, labeled): 
    fl.close()
