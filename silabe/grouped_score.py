import numpy as np
from sklearn.metrics import zero_one_score

# Input data corresponds to 4 words:
# - descalcarea (des-cal-ca-rea, predicted: de-s-cal-ca-rea)
# - somnolezi   (som-no-lezi,    predicted: som-no-lezi)
# - salandere   (sa-lan-de-re,   predicted: sa-lan-de-re)

y_pred = np.array(
    [False,  True,  True, False, False,  True, False,  True, False,
     False, False, False,  True, False,  True, False, False, False,
     False,  True, False, False,  True, False,  True, False, False,
     True,  False,  True, False,  True, False,  True, False,  True,
     False, False], dtype=bool)

y_true = np.array(
    [False, False,  True, False, False,  True, False,  True, False,
     False, False, False,  True, False,  True, False, False, False,
     False,  True, False, False,  True, False,  True, False, False,
     True, False,  True, False,  True, False,  True, False,  True,
     False, False], dtype=bool)

# maps samples to the words they belong to
groups = np.array(
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2,
     2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])


def all_or_nothing_score(y_true, y_pred, groups=None):
    y_true, y_pred = (np.asarray(y) for y in (y_true, y_pred))
    if groups is None:
        groups = np.ones_like(y_true)
    else:
        groups = np.asarray(groups)

    hits = [np.all(y_true[np.where(groups == this_group)] ==
                   y_pred[np.where(groups == this_group)])
            for this_group in np.unique(groups)]
    return np.mean(hits)


def all_or_nothing_contig(y_true, y_pred, groups):
    matches = 0
    n_groups = 0
    is_good = False
    for k, (this_y_true, this_y_pred) in enumerate(zip(y_true, y_pred)):
        if groups[k] != groups[k - 1]:
            n_groups += 1
            matches += is_good
            is_good = True
        if this_y_true != this_y_pred:
            is_good = False

    matches += is_good
    return (matches * 1.0) / n_groups


# what proportion of candidate hyphens were predicted correctly?
print zero_one_score(y_true, y_pred)  # 0.973684210526

# what proportion of words did we get completely right?
print all_or_nothing_score(y_true, y_pred, groups)  # 0.75
print all_or_nothing_contig(y_true, y_pred, groups)
