import sys
import numpy as np

n_words, n_items, word_count, item_count = 0, 0, 0, 0
trans_mat = np.zeros((8, 8), dtype=np.int)

we_good = True
pred = None
for line in open(sys.argv[1]):
    line = line.strip()
    if not line:
        n_words += 1
        pred = None
        if we_good:
            word_count += 1
        we_good = True
    else:
        n_items += 1
        old_pred = pred
        true, pred = map(int, line.split())
        if old_pred is not None:
            trans_mat[old_pred, pred] += 1
        if true == pred:
            item_count += 1
        else:
            we_good = False

print 'Item accuracy: %.4f' % (item_count * 1.0 / n_items)
print 'Word accuracy: %.4f' % (word_count * 1.0 / n_words)
print trans_mat
