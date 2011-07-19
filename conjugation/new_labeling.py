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
labeled = codecs.open('inf-ta-labeled.txt', 'w', encoding='utf-8')
rules = []
# conj 1
# a spera
              
# pt verbe cu -ta gen cânta
# (alternanta in flectiv t->ţ la 2sg)
rules.append({'1sg': u'^([a-zăâîşţ]+)t$',
              '2sg': u'^([a-zăâîşţ]+)ţi$',
              '3sg': u'^([a-zăâîşţ]+)tă$',
              '1pl': u'^([a-zăâîşţ]+)tăm$',
              '2pl': u'^([a-zăâîşţ]+)taţi$',
              '3pl': u'^([a-zăâîşţ]+)tă$'})

# (alternanta in flectiv t->ţ la 2sg)
rules.append({'1sg': u'^([a-zăâîşţ]+)st$',
              '2sg': u'^([a-zăâîşţ]+)şti$',
              '3sg': u'^([a-zăâîşţ]+)stă$',
              '1pl': u'^([a-zăâîşţ]+)stăm$',
              '2pl': u'^([a-zăâîşţ]+)staţi$',
              '3pl': u'^([a-zăâîşţ]+)stă$'})
              
# a destepta (alternanta in flectiv t->ţ la 2sg + e-ea )
rules.append({'1sg': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)t$',
              '2sg': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)ţi$',
              '3sg': u'^([a-zăâîşţ]+)ea([a-zăâîşţ]+)tă$',
              '1pl': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)tăm$',
              '2pl': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)taţi$',
              '3pl': u'^([a-zăâîşţ]+)ea([a-zăâîşţ]+)tă$'})

# a reprezenta
#rules.append({'1sg': u'^([a-zăâîşţ]+)i([a-zăâîşţ]+)t$',
#              '2sg': u'^([a-zăâîşţ]+)i([a-zăâîşţ]+)ţi$',
#              '3sg': u'^([a-zăâîşţ]+)i([a-zăâîşţ]+)tă$',
#              '1pl': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)tăm$',
#              '2pl': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)taţi$',
#              '3pl': u'^([a-zăâîşţ]+)i([a-zăâîşţ]+)tă$'})
              
# (alternanta in flectiv t->ţ la 2sg + e-ea ) deșerta
rules.append({'1sg': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)t$',
              '2sg': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)ţi$',
              '3sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)tă$',
              '1pl': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)tăm$',
              '2pl': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)taţi$',
              '3pl': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)tă$'})

# a tresălta
rules.append({'1sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)t$',
              '2sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)ţi$',
              '3sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)tă$',
              '1pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)tăm$',
              '2pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)taţi$',
              '3pl': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)tă$'})
              
# (alternanta in flectiv t->ţ la 2sg + o-oa-u)
#rules.append({'1sg': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)t$',
#              '2sg': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)ţi$',
#              '3sg': u'^([a-zăâîşţ]+)oa([a-zăâîşţ]+)tă$',
#              '1pl': u'^([a-zăâîşţ]+)u([a-zăâîşţ]+)tăm$',
#              '2pl': u'^([a-zăâîşţ]+)u([a-zăâîşţ]+)taţi$',
#              '3pl': u'^([a-zăâîşţ]+)oa([a-zăâîşţ]+)tă$'})

# (alternanta in flectiv t->ţ la 2sg + o-oa-u)
#rules.append({'1sg': u'^([a-zăâîşţ]+)ot$',
#              '2sg': u'^([a-zăâîşţ]+)oţi$',
#              '3sg': u'^([a-zăâîşţ]+)oată$',
#              '1pl': u'^([a-zăâîşţ]+)otăm$',
#              '2pl': u'^([a-zăâîşţ]+)otaţi$',
#              '3pl': u'^([a-zăâîşţ]+)oată$'})

# (alternanta in flectiv t->ţ la 2sg + căpăta)
#rules.append({'1sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)ăt$',
#              '2sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)eţi$',
#              '3sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)ătă$',
#              '1pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)ătăm$',
#              '2pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)ătaţi$',
#              '3pl': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)ătă$'})

# (alternanta in flectiv t->ţ la 2sg + ă-e-a)
rules.append({'1sg': u'^([a-zăâîşţ]+)ăt$',
              '2sg': u'^([a-zăâîşţ]+)eţi$',
              '3sg': u'^([a-zăâîşţ]+)ată$',
              '1pl': u'^([a-zăâîşţ]+)ătăm$',
              '2pl': u'^([a-zăâîşţ]+)ătaţi$',
              '3pl': u'^([a-zăâîşţ]+)ată$'})

# (alternanta in flectiv t->ţ la 2sg + ă-e-a)
#rules.append({'1sg': u'^([a-zăâîşţ]+)ăt$',
#              '2sg': u'^([a-zăâîşţ]+)ăţi$',
#              '3sg': u'^([a-zăâîşţ]+)ată$',
#              '1pl': u'^([a-zăâîşţ]+)ătăm$',
#              '2pl': u'^([a-zăâîşţ]+)ătaţi$',
#              '3pl': u'^([a-zăâîşţ]+)ată$'})
              
# pt verbe care se conjuga cu ez (cita)  (l-ai pus deja)
rules.append({'1sg': u'^([a-zăâîşţ]+)ez$',
              '2sg': u'^([a-zăâîşţ]+)ezi$',
              '3sg': u'^([a-zăâîşţ]+)ează$',
              '1pl': u'^([a-zăâîşţ]+)ăm$',
              '2pl': u'^([a-zăâîşţ]+)aţi$',
              '3pl': u'^([a-zăâîşţ]+)ează$'})

# a consta
#rules.append({'1sg': u'^([a-zăâîşţ]+)au$',
#              '2sg': u'^([a-zăâîşţ]+)ai$',
#              '3sg': u'^([a-zăâîşţ]+)ă$',
#              '1pl': u'^([a-zăâîşţ]+)ăm$',
#              '2pl': u'^([a-zăâîşţ]+)aţi$',
#              '3pl': u'^([a-zăâîşţ]+)ă$'})

words = {}

for line in f:
    word, base, persoana = line.split()
    if not base.endswith('ta'):
        continue
    if base == 'vuieta':  #wrong
        continue
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
                root = match.groups()
            elif root != match.groups():
                continue
            pers.add(persoana)

    return len(pers) >= 6

totals = len(words)
count = np.zeros(len(rules) + 1)
for base, forms in words.items():
    if len(forms) < 6:
        totals -= 1
        continue
    flags, = np.where([check(forms, rls) for rls in rules])
    flags  += 1
    matches = len(flags)
    if matches > 1:
        print base, flags
    if matches == 0:
        count[0] += 1
        label = 0
    else:
        label = flags[0]  # index of the first match 

    count[flags] += 1
    if label != 0:
        print >> labeled, u"%s\t%d" % (base, label - 1)

print "Captured: "
for i, n in enumerate(count):
    print '%d: %d' % (i, n)
print "Uncaptured: %d out of %d" % (count[0], totals)
for fl in (f, labeled): 
    fl.close()
