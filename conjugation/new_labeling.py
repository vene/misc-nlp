# -*- coding: utf-8 -*-
"""
Labeling verbs according to rules

Lists hand-made rules that cover almost all the data
and labels verbs according to the category they fit.

Created on Tue Mar 29 17:16:36 2011

@author: vene
"""

from __future__ import division
import re
import codecs

import numpy as np

f = codecs.open('verbe-indprez.txt', 'r', encoding='utf-8-sig')
labeled = codecs.open('inf-all-labeled.txt', 'w', encoding='utf-8')
unlabeled = codecs.open('inf-all-uncaptured.txt', 'w', encoding='utf-8')

rules = []
# conj 1
# a spera
rules.append({'1sg': u'^([a-zăâîşţ]+)$',
              '2sg': u'^([a-zăâîşţ]+)i$',
              '3sg': u'^([a-zăâîşţ]+)ă$',
              '1pl': u'^([a-zăâîşţ]+)ăm$',
              '2pl': u'^([a-zăâîşţ]+)aţi$',
              '3pl': u'^([a-zăâîşţ]+)ă$'})

# pt verbe gen număra
# (alternanta ă-> e la 2sg)
rules.append({'1sg': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)$',
             '2sg': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)i$',
             '3sg': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)ă$',
             '1pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)ăm$',
             '2pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)aţi$',
             '3pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)ă$'})

# pt verbe cu tr, pl, bl, fl (intra)
rules.append({'1sg': u'^([a-zăâîşţ]+)u$',
              '2sg': u'^([a-zăâîşţ]+)i$',
              '3sg': u'^([a-zăâîşţ]+)ă$',
              '1pl': u'^([a-zăâîşţ]+)ăm$',
              '2pl': u'^([a-zăâîşţ]+)aţi$',
              '3pl': u'^([a-zăâîşţ]+)ă$'})

# pt verbe care se termina in şca- mişca
rules.append({'1sg': u'^([a-zăâîşţ]+)şc$',
              '2sg': u'^([a-zăâîşţ]+)şti$',
              '3sg': u'^([a-zăâîşţ]+)şcă$',
              '1pl': u'^([a-zăâîşţ]+)şcăm$',
              '2pl': u'^([a-zăâîşţ]+)şcaţi$',
              '3pl': u'^([a-zăâîşţ]+)şcă$'})

# pt verbe gen taia (cu ia si vocala inainte)
rules.append({'1sg': u'^([a-zăâîşţ]+)$',
              '2sg': u'^([a-zăâîşţ]+)$',
              '3sg': u'^([a-zăâîşţ]+)e$',
              '1pl': u'^([a-zăâîşţ]+)em$',
              '2pl': u'^([a-zăâîşţ]+)aţi$',
              '3pl': u'^([a-zăâîşţ]+)e$'})

# pt verbe gen speria (cu ia si consoana inainte)
rules.append({'1sg': u'^([a-zăâîşţ]+)i$',
              '2sg': u'^([a-zăâîşţ]+)i$',
              '3sg': u'^([a-zăâîşţ]+)e$',
              '1pl': u'^([a-zăâîşţ]+)em$',
              '2pl': u'^([a-zăâîşţ]+)aţi$',
              '3pl': u'^([a-zăâîşţ]+)e$'})

# verbele cu -ta (cele comentate nu-s destul de productive)

# pt verbe cu -ta gen cânta
# (alternanta in flectiv t->ţ la 2sg)
rules.append({'1sg': u'^([a-zăâîşţ]+)t$',
              '2sg': u'^([a-zăâîşţ]+)ţi$',
              '3sg': u'^([a-zăâîşţ]+)tă$',
              '1pl': u'^([a-zăâîşţ]+)tăm$',
              '2pl': u'^([a-zăâîşţ]+)taţi$',
              '3pl': u'^([a-zăâîşţ]+)tă$'})

# (alternanta in flectiv t->ţ la 2sg) gen a exista
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

# (alternanta in flectiv t->ţ la 2sg + ă-e-a) desfata
rules.append({'1sg': u'^([a-zăâîşţ]+)ăt$',
              '2sg': u'^([a-zăâîşţ]+)eţi$',
              '3sg': u'^([a-zăâîşţ]+)ată$',
              '1pl': u'^([a-zăâîşţ]+)ătăm$',
              '2pl': u'^([a-zăâîşţ]+)ătaţi$',
              '3pl': u'^([a-zăâîşţ]+)ată$'})

# imbata cred (alternanta in flectiv t->ţ la 2sg + ă-e-a)
#rules.append({'1sg': u'^([a-zăâîşţ]+)ăt$',
#              '2sg': u'^([a-zăâîşţ]+)ăţi$',
#              '3sg': u'^([a-zăâîşţ]+)ată$',
#              '1pl': u'^([a-zăâîşţ]+)ătăm$',
#              '2pl': u'^([a-zăâîşţ]+)ătaţi$',
#              '3pl': u'^([a-zăâîşţ]+)ată$'})
              
# pt verbe care se conjuga cu ez (cita)  (e pus pentru dansa mai jos)
#rules.append({'1sg': u'^([a-zăâîşţ]+)ez$',
#             '2sg': u'^([a-zăâîşţ]+)ezi$',
#             '3sg': u'^([a-zăâîşţ]+)ează$',
#             '1pl': u'^([a-zăâîşţ]+)ăm$',
#             '2pl': u'^([a-zăâîşţ]+)aţi$',
#             '3pl': u'^([a-zăâîşţ]+)ează$'})

# a consta
#rules.append({'1sg': u'^([a-zăâîşţ]+)au$',
#              '2sg': u'^([a-zăâîşţ]+)ai$',
#              '3sg': u'^([a-zăâîşţ]+)ă$',
#              '1pl': u'^([a-zăâîşţ]+)ăm$',
#              '2pl': u'^([a-zăâîşţ]+)aţi$',
#              '3pl': u'^([a-zăâîşţ]+)ă$'})

# pt verbe care se conjuga cu ez (dansa)  
rules.append({'1sg': u'^([a-zăâîşţ]+)ez$',
              '2sg': u'^([a-zăâîşţ]+)ezi$',
              '3sg': u'^([a-zăâîşţ]+)ează$',
              '1pl': u'^([a-zăâîşţ]+)ăm$',
              '2pl': u'^([a-zăâîşţ]+)aţi$',
              '3pl': u'^([a-zăâîşţ]+)ează$'})

# pt verbe care se conjuga cu ez si au ia la inf (copia) 
rules.append({'1sg': u'^([a-zăâîşţ]+)ez$',
              '2sg': u'^([a-zăâîşţ]+)ezi$',
              '3sg': u'^([a-zăâîşţ]+)ază$',
              '1pl': u'^([a-zăâîşţ]+)em$',
              '2pl': u'^([a-zăâîşţ]+)aţi$',
              '3pl': u'^([a-zăâîşţ]+)ază$'})

# pt verbe cu ca la inf (parca, şoca) si ez
rules.append({'1sg': u'^([a-zăâîşţ]+)hez$',
              '2sg': u'^([a-zăâîşţ]+)hezi$',
              '3sg': u'^([a-zăâîşţ]+)hează$',
              '1pl': u'^([a-zăâîşţ]+)ăm$',
              '2pl': u'^([a-zăâîşţ]+)aţi$',
              '3pl': u'^([a-zăâîşţ]+)hează$'})

# conj a 2a (infinitivul in -ea)
# ->la fel ca primul pattern de la conj a 3a

# pt verbele care au alternanta ă->a in radical, "a părea"
rules.append({'1sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)$',
              '2sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)i$',
              '3sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)e$',
              '1pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)em$',
              '2pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)eţi$',
              '3pl': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)$'})

#a vedea și altele
rules.append({'1sg': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]*)d$',
              '2sg': u'^([a-zăâîşţ]+)e([a-zăâîşţ]*)zi$',
              '3sg': u'^([a-zăâîşţ]+)e([a-zăâîşţ]*)de$',
              '1pl': u'^([a-zăâîşţ]+)e([a-zăâîşţ]*)dem$',
              '2pl': u'^([a-zăâîşţ]+)e([a-zăâîşţ]*)deţi$',
              '3pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]*)d$'})

#NOU! pt verbe gen "a cădea" si derivatele; alternanta ca mai sus + d->z
rules.append({'1sg': u'^([a-zăâîşţ]+)ad$',
              '2sg': u'^([a-zăâîşţ]+)azi$',
              '3sg': u'^([a-zăâîşţ]+)ade$',
              '1pl': u'^([a-zăâîşţ]+)ădem$',
              '2pl': u'^([a-zăâîşţ]+)ădeţi$',
              '3pl': u'^([a-zăâîşţ]+)ad$'})
              
# NOU! "a urechea", "a veghea" care se conjuga cu ez; difera de ez-ul de la 1   
rules.append({'1sg': u'^([a-zăâîşţ]+)ez$',
              '2sg': u'^([a-zăâîşţ]+)ezi$',
              '3sg': u'^([a-zăâîşţ]+)ează$',
              '1pl': u'^([a-zăâîşţ]+)em$',
              '2pl': u'^([a-zăâîşţ]+)eaţi$',
              '3pl': u'^([a-zăâîşţ]+)ează$'})
              
# conj a 3a (infinitivul in -e)
#in general
rules.append({'1sg': u'^([a-zăâîşţ]+)$',
              '2sg': u'^([a-zăâîşţ]+)i$',
              '3sg': u'^([a-zăâîşţ]+)e$',
              '1pl': u'^([a-zăâîşţ]+)em$',
              '2pl': u'^([a-zăâîşţ]+)eţi$',
              '3pl': u'^([a-zăâîşţ]+)$'})
#a comite t->ţ
rules.append({'1sg': u'^([a-zăâîşţ]+)t$',
              '2sg': u'^([a-zăâîşţ]+)ţi$',
              '3sg': u'^([a-zăâîşţ]+)te$',
              '1pl': u'^([a-zăâîşţ]+)tem$',
              '2pl': u'^([a-zăâîşţ]+)teţi$',
              '3pl': u'^([a-zăâîşţ]+)t$'})

# a scrie
rules.append({'1sg': u'^([a-zăâîşţ]+)u$',
              '2sg': u'^([a-zăâîşţ]+)i$',
              '3sg': u'^([a-zăâîşţ]+)e$',
              '1pl': u'^([a-zăâîşţ]+)em$',
              '2pl': u'^([a-zăâîşţ]+)eţi$',
              '3pl': u'^([a-zăâîşţ]+)u$'})

# pt -şte la infinitiv (naşte, paşte)
rules.append({'1sg': u'^([a-zăâîşţ]+)sc$',
              '2sg': u'^([a-zăâîşţ]+)şti$',
              '3sg': u'^([a-zăâîşţ]+)şte$',
              '1pl': u'^([a-zăâîşţ]+)ştem$',
              '2pl': u'^([a-zăâîşţ]+)şteţi$',
              '3pl': u'^([a-zăâîşţ]+)sc$'})

# pt -ne la infinitiv (l-ai pus deja) ex: a pune
rules.append({'1sg': u'^([a-zăâîşţ]+)n$', 
              '2sg': u'^([a-zăâîşţ]+)i$',
              '3sg': u'^([a-zădâîşţ]+)ne$',
              '1pl': u'^([a-zăâîşţ]+)nem$',
              '2pl': u'^([a-zăâîşţ]+)neţi$',
              '3pl': u'^([a-zăâîşţ]+)n$'})

#pt a crede
rules.append({'1sg': u'^([a-zăâîşţ]+)d$',
              '2sg': u'^([a-zăâîşţ]+)zi$',
              '3sg': u'^([a-zăâîşţ]+)de$',
              '1pl': u'^([a-zăâîşţ]+)dem$',
              '2pl': u'^([a-zăâîşţ]+)deţi$',
              '3pl': u'^([a-zăâîşţ]+)d$'})

# conj a 4a

# # pt verbe ca a fugi
# rules.append({'1sg': u'^([a-zăâîşţ]+)$',
#               '2sg': u'^([a-zăâîşţ]+)i$',
#               '3sg': u'^([a-zăâîşţ]+)e$',
#               '1pl': u'^([a-zăâîşţ]+)im$',
#               '2pl': u'^([a-zăâîşţ]+)iţi$',
#               '3pl': u'^([a-zăâîşţ]+)$'})

# pt verbe cu ui, âi, ăi (sui)
rules.append({'1sg': u'^([a-zăâîşţ]+)i$',
              '2sg': u'^([a-zăâîşţ]+)i$',
              '3sg': u'^([a-zăâîşţ]+)ie$',
              '1pl': u'^([a-zăâîşţ]+)im$',
              '2pl': u'^([a-zăâîşţ]+)iţi$',
              '3pl': u'^([a-zăâîşţ]+)ie$'})

# pt verbe care se conjuga cu esc (vorbi, citi) 
rules.append({'1sg': u'^([a-zăâîşţ]+)esc$',
              '2sg': u'^([a-zăâîşţ]+)eşti$',
              '3sg': u'^([a-zăâîşţ]+)eşte$',
              '1pl': u'^([a-zăâîşţ]+)im$',
              '2pl': u'^([a-zăâîşţ]+)iţi$',
              '3pl': u'^([a-zăâîşţ]+)esc$'})

# pt verbe cu esc care se termina in ui, ăi, oi(locui)
rules.append({'1sg': u'^([a-zăâîşţ]+)iesc$',
              '2sg': u'^([a-zăâîşţ]+)ieşti$',
              '3sg': u'^([a-zăâîşţ]+)ieşte$',
              '1pl': u'^([a-zăâîşţ]+)im$',
              '2pl': u'^([a-zăâîşţ]+)iţi$',
              '3pl': u'^([a-zăâîşţ]+)iesc$'})

#pt verbele care se termina cu î la inf (omorî) 
rules.append({'1sg': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)$',
              '2sg': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)i$',
              '3sg': u'^([a-zăâîşţ]+)oa([a-zăâîşţ]+)ă$',
              '1pl': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)âm$',
              '2pl': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)âţi$',
              '3pl': u'^([a-zăâîşţ]+)oa([a-zăâîşţ]+)ă$'})

# pt verbele cu î si ăsc (hotărî)
rules.append({'1sg': u'^([a-zăâîşţ]+)ăsc$',
              '2sg': u'^([a-zăâîşţ]+)ăşti$',
              '3sg': u'^([a-zăâîşţ]+)ăşte$',
              '1pl': u'^([a-zăâîşţ]+)âm$',
              '2pl': u'^([a-zăâîşţ]+)âţi$',
              '3pl': u'^([a-zăâîşţ]+)ăsc$'})

words = {}

print "Loading data in memory...",
for line in f:
    word, base, persoana = line.split()
    persoana = persoana.split(".")[3]
    if words.has_key(base):
        words[base].append((word, persoana))  # 3pl
    else:
        words[base] = [(word, persoana)]

print "done"

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


count = np.zeros(len(rules))
uncaptured = 0
for base, forms in words.items():
    label_ez = 0
    label_esc = 0
    flags, = np.where([check(forms, rls) for rls in rules])
    
    matches = len(flags)
    if matches > 1:
        print base, flags
    if matches == 0:
        uncaptured += 1
        label = 0
        print >> unlabeled, base
    else:
        label = 1 + flags[0]  # index of the first match 

    count[flags] += 1

    print >> labeled, u"%s\t%d" % (base, label)

print "Captured: "
for i, n in enumerate(count):
    print '%d: %d' % (i, n)
print "Uncaptured: %d out of %d" % (uncaptured, len(words))
for fl in (f, labeled, unlabeled): 
    fl.close()
