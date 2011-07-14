# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 17:16:36 2011

@author: vene
"""

from __future__ import division
import re
import codecs

f = codecs.open('verbe-indprez.txt', 'r', encoding='utf-8-sig')
g = codecs.open('inf-doar-ez.txt', 'w', encoding='utf-8')
labeled = codecs.open('inf-ez-labeled.txt', 'w', encoding='utf-8')
h = codecs.open('inf-doar-esc.txt', 'w', encoding='utf-8')
esclabeled = codecs.open('inf-esc-labeled.txt', 'w', encoding='utf-8')

rules_a = {'1sg': u'^([a-zăâîşţ]+)ez$',
         '2sg': u'^([a-zăâîşţ]+)ezi$',
         '3sg': u'^([a-zăâîşţ]+)ază$',
         '1pl': u'^([a-zăâîşţ]+)em$',
         '2pl': u'^([a-zăâîşţ]+)aţi$',
         '3pl': u'^([a-zăâîşţ]+)ază$'}

rules_b = {'1sg': u'^([a-zăâîşţ]+)ez$',
         '2sg': u'^([a-zăâîşţ]+)ezi$',
         '3sg': u'^([a-zăâîşţ]+)ează$',
         '1pl': u'^([a-zăâîşţ]+)ăm$',
         '2pl': u'^([a-zăâîşţ]+)aţi$',
         '3pl': u'^([a-zăâîşţ]+)ează$'}

rules_c = {'1sg': u'^([a-zăâîşţ]+)esc$',
         '2sg': u'^([a-zăâîşţ]+)eşti$',
         '3sg': u'^([a-zăâîşţ]+)eşte$',
         '1pl': u'^([a-zăâîşţ]+)im$',
         '2pl': u'^([a-zăâîşţ]+)iţi$',
         '3pl': u'^([a-zăâîşţ]+)esc$'}

words = {}

for line in f:
    word, base, persoana = line.split()
#    word = unicode(word, "utf-8-sig")
#    base = unicode(base, "utf-8-sig")
    persoana = persoana.split(".")[3]
    if words.has_key(base):
        words[base].append((word, persoana)) #  3pl
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


count_ez = count_esc = 0
for base, forms in words.items():
    label_ez = 0
    label_esc = 0
    is_a = check(forms, rules_a)
    is_b = check(forms, rules_b)
    is_c = check(forms, rules_c)
    if is_c:
        count_esc += 1
        label_esc = 1
        print >> h, base
    elif is_a or is_b:
        count_ez += 1
        label_ez = 1 if is_a else 2
        print >> g, base

    print >> labeled, u"%s\t%d" % (base, label_ez)
    print >> esclabeled, u"%s\t%d" % (base, label_esc)

print "Captured: %d(ez)+%d(esc)" % (count_ez, count_esc)
print "out of %d" % len(words)
for fl in (f, g, labeled): 
    fl.close()
