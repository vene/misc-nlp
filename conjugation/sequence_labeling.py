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

from crfsuite_utils import crfsuite_features

f = codecs.open('verbe-indprez.txt', 'r', encoding='utf-8-sig')
#labeled = codecs.open('inf-all-labeled.txt', 'w', encoding='utf-8')
#unlabeled = codecs.open('inf-all-uncaptured.txt', 'w', encoding='utf-8')

rules = []
# conj 1
# a spera
rules.append(({'1sg': u'^([a-zăâîşţ]+)$',
              '2sg': u'^([a-zăâîşţ]+)i$',
              '3sg': u'^([a-zăâîşţ]+)ă$',
              '1pl': u'^([a-zăâîşţ]+)ăm$',
              '2pl': u'^([a-zăâîşţ]+)aţi$',
              '3pl': u'^([a-zăâîşţ]+)ă$'},
              ['T1']))

# pt verbe gen număra
# (alternanta ă-> e la 2sg)
rules.append(({'1sg': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)$',
             '2sg': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)i$',
             '3sg': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)ă$',
             '1pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)ăm$',
             '2pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)aţi$',
             '3pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)ă$'},
             ['a2', 'T1']))

# pt verbe cu tr, pl, bl, fl (intra)
rules.append(({'1sg': u'^([a-zăâîşţ]+)u$',
              '2sg': u'^([a-zăâîşţ]+)i$',
              '3sg': u'^([a-zăâîşţ]+)ă$',
              '1pl': u'^([a-zăâîşţ]+)ăm$',
              '2pl': u'^([a-zăâîşţ]+)aţi$',
              '3pl': u'^([a-zăâîşţ]+)ă$'},
              ['T2']))

# pt verbe care se termina in şca- mişca
# sh intra in paranteza, cel mai bine

rules.append(({'1sg': u'^([a-zăâîşţ]+)şc$',
              '2sg': u'^([a-zăâîşţ]+)şti$',
              '3sg': u'^([a-zăâîşţ]+)şcă$',
              '1pl': u'^([a-zăâîşţ]+)şcăm$',
              '2pl': u'^([a-zăâîşţ]+)şcaţi$',
              '3pl': u'^([a-zăâîşţ]+)şcă$'},
              ['0', 'c0', 'T1']))

# pt verbe gen taia (cu ia si vocala inainte)
rules.append(({'1sg': u'^([a-zăâîşţ]+)$',
              '2sg': u'^([a-zăâîşţ]+)$',
              '3sg': u'^([a-zăâîşţ]+)e$',
              '1pl': u'^([a-zăâîşţ]+)em$',
              '2pl': u'^([a-zăâîşţ]+)aţi$',
              '3pl': u'^([a-zăâîşţ]+)e$'},
              ['T3']))

# pt verbe gen speria (cu ia si consoana inainte)
rules.append(({'1sg': u'^([a-zăâîşţ]+)i$',
              '2sg': u'^([a-zăâîşţ]+)i$',
              '3sg': u'^([a-zăâîşţ]+)e$',
              '1pl': u'^([a-zăâîşţ]+)em$',
              '2pl': u'^([a-zăâîşţ]+)aţi$',
              '3pl': u'^([a-zăâîşţ]+)e$'},
              ['T4']))

# verbele cu -ta (cele comentate nu-s destul de productive)

# pt verbe cu -ta gen cânta
# (alternanta in flectiv t->ţ la 2sg)
rules.append(({'1sg': u'^([a-zăâîşţ]+)t$',
              '2sg': u'^([a-zăâîşţ]+)ţi$',
              '3sg': u'^([a-zăâîşţ]+)tă$',
              '1pl': u'^([a-zăâîşţ]+)tăm$',
              '2pl': u'^([a-zăâîşţ]+)taţi$',
              '3pl': u'^([a-zăâîşţ]+)tă$'},
              ['t0', 'T1']))


# (alternanta in flectiv t->ţ la 2sg) gen a exista
rules.append(({'1sg': u'^([a-zăâîşţ]+)st$',
              '2sg': u'^([a-zăâîşţ]+)şti$',
              '3sg': u'^([a-zăâîşţ]+)stă$',
              '1pl': u'^([a-zăâîşţ]+)stăm$',
              '2pl': u'^([a-zăâîşţ]+)staţi$',
              '3pl': u'^([a-zăâîşţ]+)stă$'},
              ['s0', 'T1', 'T1']))

# a destepta (alternanta in flectiv t->ţ la 2sg + e-ea )
rules.append(({'1sg': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)t$',
              '2sg': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)ţi$',
              '3sg': u'^([a-zăâîşţ]+)ea([a-zăâîşţ]+)tă$',
              '1pl': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)tăm$',
              '2pl': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)taţi$',
              '3pl': u'^([a-zăâîşţ]+)ea([a-zăâîşţ]+)tă$'},
              ['e0', 't0', 'T1']))

# a reprezenta
rules.append(({'1sg': u'^([a-zăâîşţ]+)i([a-zăâîşţ]+)t$',
              '2sg': u'^([a-zăâîşţ]+)i([a-zăâîşţ]+)ţi$',
              '3sg': u'^([a-zăâîşţ]+)i([a-zăâîşţ]+)tă$',
              '1pl': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)tăm$',
              '2pl': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)taţi$',
              '3pl': u'^([a-zăâîşţ]+)i([a-zăâîşţ]+)tă$'},
              ['e1', 't0', 'T1']))

# (alternanta in flectiv t->ţ la 2sg + e-ea ) deșerta
rules.append(({'1sg': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)t$',
              '2sg': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)ţi$',
              '3sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)tă$',
              '1pl': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)tăm$',
              '2pl': u'^([a-zăâîşţ]+)e([a-zăâîşţ]+)taţi$',
              '3pl': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)tă$'},
              ['e2', 't0', 'T1']))

# a tresălta
rules.append(({'1sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)t$',
              '2sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)ţi$',
              '3sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)tă$',
              '1pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)tăm$',
              '2pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)taţi$',
              '3pl': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)tă$'},
              ['a0', 't0', 'T1']))

# (alternanta in flectiv t->ţ la 2sg + o-oa-u) a purta
rules.append(({'1sg': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)t$',
              '2sg': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)ţi$',
              '3sg': u'^([a-zăâîşţ]+)oa([a-zăâîşţ]+)tă$',
              '1pl': u'^([a-zăâîşţ]+)u([a-zăâîşţ]+)tăm$',
              '2pl': u'^([a-zăâîşţ]+)u([a-zăâîşţ]+)taţi$',
              '3pl': u'^([a-zăâîşţ]+)oa([a-zăâîşţ]+)tă$'},
              ['u0', 't0', 'T1']))

# (alternanta in flectiv t->ţ la 2sg + o-oa-u) a înota
rules.append(({'1sg': u'^([a-zăâîşţ]+)ot$',
              '2sg': u'^([a-zăâîşţ]+)oţi$',
              '3sg': u'^([a-zăâîşţ]+)oată$',
              '1pl': u'^([a-zăâîşţ]+)otăm$',
              '2pl': u'^([a-zăâîşţ]+)otaţi$',
              '3pl': u'^([a-zăâîşţ]+)oată$'},
              ['o0', 't0', 'T1']))

# (alternanta in flectiv t->ţ la 2sg + căpăta)
rules.append(({'1sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)ăt$',
              '2sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)eţi$',
              '3sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)ătă$',
              '1pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)ătăm$',
              '2pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)ătaţi$',
              '3pl': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)ătă$'},
              ['a0', 'a2', 't0', 'T1']))

# (alternanta in flectiv t->ţ la 2sg + ă-e-a) desfata
rules.append(({'1sg': u'^([a-zăâîşţ]+)ăt$',
              '2sg': u'^([a-zăâîşţ]+)eţi$',
              '3sg': u'^([a-zăâîşţ]+)ată$',
              '1pl': u'^([a-zăâîşţ]+)ătăm$',
              '2pl': u'^([a-zăâîşţ]+)ătaţi$',
              '3pl': u'^([a-zăâîşţ]+)ată$'},
              ['a1', 't0', 'T1']))

# ??? (alternanta in flectiv t->ţ la 2sg + ă-e-a)
rules.append(({'1sg': u'^([a-zăâîşţ]+)ăt$',
              '2sg': u'^([a-zăâîşţ]+)ăţi$',
              '3sg': u'^([a-zăâîşţ]+)ată$',
              '1pl': u'^([a-zăâîşţ]+)ătăm$',
              '2pl': u'^([a-zăâîşţ]+)ătaţi$',
              '3pl': u'^([a-zăâîşţ]+)ată$'},
              ['a4', 't0', 'T1']))

# a consta
rules.append(({'1sg': u'^([a-zăâîşţ]+)au$',
              '2sg': u'^([a-zăâîşţ]+)ai$',
              '3sg': u'^([a-zăâîşţ]+)ă$',
              '1pl': u'^([a-zăâîşţ]+)ăm$',
              '2pl': u'^([a-zăâîşţ]+)aţi$',
              '3pl': u'^([a-zăâîşţ]+)ă$'},
              ['a5', 'T2']))  # la fel de bine poate fi au-a- - - - + T1,
                              # de vazut care din ele mai apare in rest!

# pt verbe care se conjuga cu ez (dansa)
rules.append(({'1sg': u'^([a-zăâîşţ]+)ez$',
              '2sg': u'^([a-zăâîşţ]+)ezi$',
              '3sg': u'^([a-zăâîşţ]+)ează$',
              '1pl': u'^([a-zăâîşţ]+)ăm$',
              '2pl': u'^([a-zăâîşţ]+)aţi$',
              '3pl': u'^([a-zăâîşţ]+)ează$'},
              ['T5']))

# pt verbe care se conjuga cu ez si au ia la inf (copia)
rules.append(({'1sg': u'^([a-zăâîşţ]+)ez$',
              '2sg': u'^([a-zăâîşţ]+)ezi$',
              '3sg': u'^([a-zăâîşţ]+)ază$',
              '1pl': u'^([a-zăâîşţ]+)em$',
              '2pl': u'^([a-zăâîşţ]+)aţi$',
              '3pl': u'^([a-zăâîşţ]+)ază$'},
              ['T6']))

# pt verbe cu ca la inf (parca, şoca) si ez
rules.append(({'1sg': u'^([a-zăâîşţ]+)hez$',
              '2sg': u'^([a-zăâîşţ]+)hezi$',
              '3sg': u'^([a-zăâîşţ]+)hează$',
              '1pl': u'^([a-zăâîşţ]+)ăm$',
              '2pl': u'^([a-zăâîşţ]+)aţi$',
              '3pl': u'^([a-zăâîşţ]+)hează$'},
              ['T7']))

# conj a 2a (infinitivul in -ea)
# ->la fel ca primul pattern de la conj a 3a

# pt verbele care au alternanta ă->a in radical, "a părea"
rules.append(({'1sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)$',
              '2sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)i$',
              '3sg': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)e$',
              '1pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)em$',
              '2pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]+)eţi$',
              '3pl': u'^([a-zăâîşţ]+)a([a-zăâîşţ]+)$'},
              ['a0', 'T8']))

#a vedea și altele
rules.append(({'1sg': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]*)d$',
              '2sg': u'^([a-zăâîşţ]+)e([a-zăâîşţ]*)zi$',
              '3sg': u'^([a-zăâîşţ]+)e([a-zăâîşţ]*)de$',
              '1pl': u'^([a-zăâîşţ]+)e([a-zăâîşţ]*)dem$',
              '2pl': u'^([a-zăâîşţ]+)e([a-zăâîşţ]*)deţi$',
              '3pl': u'^([a-zăâîşţ]+)ă([a-zăâîşţ]*)d$'},
              ['e3', 'd0', 'T8']))

#NOU! pt verbe gen "a cădea" si derivatele; alternanta ca mai sus + d->z
rules.append(({'1sg': u'^([a-zăâîşţ]+)ad$',
              '2sg': u'^([a-zăâîşţ]+)azi$',
              '3sg': u'^([a-zăâîşţ]+)ade$',
              '1pl': u'^([a-zăâîşţ]+)ădem$',
              '2pl': u'^([a-zăâîşţ]+)ădeţi$',
              '3pl': u'^([a-zăâîşţ]+)ad$'},
              ['a0', 'd0', 'T8']))

# NOU! "a urechea", "a veghea" care se conjuga cu ez; difera de ez-ul de la 1
rules.append(({'1sg': u'^([a-zăâîşţ]+)ez$',
              '2sg': u'^([a-zăâîşţ]+)ezi$',
              '3sg': u'^([a-zăâîşţ]+)ează$',
              '1pl': u'^([a-zăâîşţ]+)em$',
              '2pl': u'^([a-zăâîşţ]+)eaţi$',
              '3pl': u'^([a-zăâîşţ]+)ează$'},
              ['T16']))

# conj a 3a (infinitivul in -e)
#in general
rules.append(({'1sg': u'^([a-zăâîşţ]+)$',
              '2sg': u'^([a-zăâîşţ]+)i$',
              '3sg': u'^([a-zăâîşţ]+)e$',
              '1pl': u'^([a-zăâîşţ]+)em$',
              '2pl': u'^([a-zăâîşţ]+)eţi$',
              '3pl': u'^([a-zăâîşţ]+)$'},
              ['T8']))
#a comite t->ţ
rules.append(({'1sg': u'^([a-zăâîşţ]+)t$',
              '2sg': u'^([a-zăâîşţ]+)ţi$',
              '3sg': u'^([a-zăâîşţ]+)te$',
              '1pl': u'^([a-zăâîşţ]+)tem$',
              '2pl': u'^([a-zăâîşţ]+)teţi$',
              '3pl': u'^([a-zăâîşţ]+)t$'},
              ['t0', 'T8']))

# a scrie
rules.append(({'1sg': u'^([a-zăâîşţ]+)u$',
              '2sg': u'^([a-zăâîşţ]+)i$',
              '3sg': u'^([a-zăâîşţ]+)e$',
              '1pl': u'^([a-zăâîşţ]+)em$',
              '2pl': u'^([a-zăâîşţ]+)eţi$',
              '3pl': u'^([a-zăâîşţ]+)u$'},
              ['T9']))  # DE CE NU E u1, T8?

# pt -şte la infinitiv (naşte, paşte)
rules.append(({'1sg': u'^([a-zăâîşţ]+)sc$',
              '2sg': u'^([a-zăâîşţ]+)şti$',
              '3sg': u'^([a-zăâîşţ]+)şte$',
              '1pl': u'^([a-zăâîşţ]+)ştem$',
              '2pl': u'^([a-zăâîşţ]+)şteţi$',
              '3pl': u'^([a-zăâîşţ]+)sc$'},
              ['s1', 't1', 'T8']))

# pt -ne la infinitiv ex: a pune
rules.append(({'1sg': u'^([a-zăâîşţ]+)n$',
              '2sg': u'^([a-zăâîşţ]+)i$',
              '3sg': u'^([a-zădâîşţ]+)ne$',
              '1pl': u'^([a-zăâîşţ]+)nem$',
              '2pl': u'^([a-zăâîşţ]+)neţi$',
              '3pl': u'^([a-zăâîşţ]+)n$'},
              ['n0', 'T8']))

#pt a crede
rules.append(({'1sg': u'^([a-zăâîşţ]+)d$',
              '2sg': u'^([a-zăâîşţ]+)zi$',
              '3sg': u'^([a-zăâîşţ]+)de$',
              '1pl': u'^([a-zăâîşţ]+)dem$',
              '2pl': u'^([a-zăâîşţ]+)deţi$',
              '3pl': u'^([a-zăâîşţ]+)d$'},
              ['d0', 'T8']))

# conj a 4a

# # pt verbe ca a fugi
rules.append(({'1sg': u'^([a-zăâîşţ]+)$',
              '2sg': u'^([a-zăâîşţ]+)i$',
              '3sg': u'^([a-zăâîşţ]+)e$',
              '1pl': u'^([a-zăâîşţ]+)im$',
              '2pl': u'^([a-zăâîşţ]+)iţi$',
              '3pl': u'^([a-zăâîşţ]+)$'},
              ['T10']))

# pt verbe cu ui, âi, ăi (sui)
rules.append(({'1sg': u'^([a-zăâîşţ]+)i$',
              '2sg': u'^([a-zăâîşţ]+)i$',
              '3sg': u'^([a-zăâîşţ]+)ie$',
              '1pl': u'^([a-zăâîşţ]+)im$',
              '2pl': u'^([a-zăâîşţ]+)iţi$',
              '3pl': u'^([a-zăâîşţ]+)ie$'},
              ['T11']))  # sau poate i- -i- - -ie, mai exista dovezi?

# pt verbe care se conjuga cu esc (vorbi, citi)
rules.append(({'1sg': u'^([a-zăâîşţ]+)esc$',
              '2sg': u'^([a-zăâîşţ]+)eşti$',
              '3sg': u'^([a-zăâîşţ]+)eşte$',
              '1pl': u'^([a-zăâîşţ]+)im$',
              '2pl': u'^([a-zăâîşţ]+)iţi$',
              '3pl': u'^([a-zăâîşţ]+)esc$'},
              ['T12']))

# pt verbe cu esc care se termina in ui, ăi, oi(locui)
rules.append(({'1sg': u'^([a-zăâîşţ]+)iesc$',
              '2sg': u'^([a-zăâîşţ]+)ieşti$',
              '3sg': u'^([a-zăâîşţ]+)ieşte$',
              '1pl': u'^([a-zăâîşţ]+)im$',
              '2pl': u'^([a-zăâîşţ]+)iţi$',
              '3pl': u'^([a-zăâîşţ]+)iesc$'},
              ['T13']))  # sau i care dispare + T12?

#pt verbele care se termina cu î la inf (omorî)
rules.append(({'1sg': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)$',
              '2sg': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)i$',
              '3sg': u'^([a-zăâîşţ]+)oa([a-zăâîşţ]+)ă$',
              '1pl': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)âm$',
              '2pl': u'^([a-zăâîşţ]+)o([a-zăâîşţ]+)âţi$',
              '3pl': u'^([a-zăâîşţ]+)oa([a-zăâîşţ]+)ă$'},
              ['o0', 'T15']))

# pt verbele cu î si ăsc (hotărî)
rules.append(({'1sg': u'^([a-zăâîşţ]+)ăsc$',
              '2sg': u'^([a-zăâîşţ]+)ăşti$',
              '3sg': u'^([a-zăâîşţ]+)ăşte$',
              '1pl': u'^([a-zăâîşţ]+)âm$',
              '2pl': u'^([a-zăâîşţ]+)âţi$',
              '3pl': u'^([a-zăâîşţ]+)ăsc$'},
              ['T14']))

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
    labeled = []
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
                    labeled.append((base, tagged_inf))
                    found = True
                total_time += time() - t0
                break
        if not found:
            unlabeled.append((base, [''] * len(base)))
    print '%f verbs per second.' % (total_time / len(words))
    print 'Generating crfsuite features...'
    crfsuite_features(build_instances(labeled), size=3, outfile='crf.labeled.3.txt')
    crfsuite_features(build_instances(unlabeled), size=3, outfile='crf.unlabeled.3.txt')
