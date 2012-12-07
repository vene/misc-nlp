import re
from collections import defaultdict

import numpy as np

re_tag = '(.+): \((.+?), (.+?), (.+?)\) \(.+\)'
re_item = 'Item accuracy: (.+?) / (.+?) \('
re_inst = 'Instance accuracy: .* \((.+)\)'

res = defaultdict(lambda: np.zeros(3))
item_acc = []
item_counts = []
instance_acc = []

for line in open('loo.3.last.ap.txt'):
    m = re.match(re_tag, line)
    if m:
        label, hits, model, data = m.groups()
        label = label.strip()
        hits, model, data = map(lambda x: int(x.strip()), (hits, model, data))
        res[label] += np.array([hits, model, data])
    m = re.match(re_item, line)
    if m:
        item_acc.append(int(m.groups()[0].strip()))
        item_counts.append(int(m.groups()[1].strip()))
    m = re.match(re_inst, line)
    if m:
        instance_acc.append(float(m.groups()[0].strip()))

print 'Instance accuracy: %.4f' % np.mean(instance_acc)
print 'Item accuracy: %.4f' % (np.sum(item_acc) * 1.0 / np.sum(item_counts))

print 'label \t&\tprecis\t&\trecall\t&\tcounts\t\\\\'
for key, val in sorted(res.iteritems()):
    print '%s\t&\t%.4f\t&\t%.4f\t&\t%d\t\\\\' % (
        key,
        val[0] / val[1],
        val[0] / val[2],
        val[2]
    )
