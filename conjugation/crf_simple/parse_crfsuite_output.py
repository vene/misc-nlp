import sys
import re
from collections import defaultdict

import numpy as np


def parse_crfsuite_log(lines):
    """Computes cross-validated scores from crfsuite log file.

    This is ridiculously missing from crfsuite.  Basically this accepts any
    set of lines that form the output of commands like:
        crfsuite learn -g 10 -x

    and aggregates scores.
    """

    re_tag = '(.+): \((.+?), (.+?), (.+?)\) \(.+\)'
    re_item = 'Item accuracy: (.+?) / (.+?) \('
    re_inst = 'Instance accuracy: .* \((.+)\)'

    res = defaultdict(lambda: np.zeros(3))
    fold_res = defaultdict(lambda: np.zeros(3))
    item_acc = []
    zero_acc = []
    zero_counts = []
    item_counts = []
    instance_acc = []
    fold_item_acc, fold_item_counts, fold_instance_acc = None, None, None

    for line in lines:
        # go through the file line by line
        # If it starts with this, clear label counters
        if line.startswith("***** Iteration"):
            fold_res.clear()
            continue
        # If it starts like this, it means it's the final fold statistics
        if line.startswith("Total seconds"):
            item_acc.append(fold_item_acc)
            item_counts.append(fold_item_counts)
            instance_acc.append(fold_instance_acc)
            zero_acc.append(fold_res['0'][0])
            zero_counts.append(fold_res['0'][2])
            for lbl in fold_res:
                res[lbl] += fold_res[lbl]

        # match label statistics
        m = re.match(re_tag, line)
        if m:
            label, hits, model, data = m.groups()
            label = label.strip()
            hits, model, data = map(lambda x: int(x.strip()),
                                    (hits, model, data))
            fold_res[label] += np.array([hits, model, data])
        # match accuracy statistics
        m = re.match(re_item, line)
        if m:
            fold_item_acc = int(m.groups()[0].strip())
            fold_item_counts = int(m.groups()[1].strip())
        # match instance accuracy statistics
        m = re.match(re_inst, line)
        if m:
            fold_instance_acc = float(m.groups()[0].strip())

    return instance_acc, item_acc, item_counts, zero_acc, zero_counts, res


if __name__ == "__main__":
    log_file = open(sys.argv[1])
    instance_acc, item_acc, item_counts, res = parse_crfsuite_log(log_file)
    print 'Instance accuracy: %.4f' % np.mean(instance_acc)
    print 'Item accuracy: %.4f' % (np.sum(item_acc) * 1. / np.sum(item_counts))

    print 'label \t&\tprecis\t&\trecall\t&\tcounts\t\\\\'
    for key, val in sorted(res.iteritems()):
        print '%s\t&\t%.4f\t&\t%.4f\t&\t%d\t\\\\' % (
            key,
            val[0] / val[1],
            val[0] / val[2],
            val[2]
        )
