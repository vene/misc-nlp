import os
import numpy as np

from parse_crfsuite_output import parse_crfsuite_log


def optimized_scores((instance_acc, item_acc, item_cnt, zero_acc, zero_cnt, l)):
    return (np.mean(instance_acc),
            np.mean([(item_a - zero_a) * 1. / (item_c - zero_c)
                     for (item_a, zero_a, item_c, zero_c) in zip(
                         item_acc, zero_acc, item_cnt, zero_cnt)]),
            (np.sum(item_acc) * 1. / np.sum(item_cnt)))


if __name__ == '__main__':
    # l-bfgs:
    lbfgs_list = []
    for f_name in os.listdir('lbfgs_logs'):
        ps, pt, n, c = f_name.split(".", 3)
        ps = ps[-1]
        pt = pt[-1]
        ps, pt, n, c = map(float, (ps, pt, n, c))
        with open(os.path.join('lbfgs_logs', f_name)) as f:
            acc = optimized_scores(parse_crfsuite_log(f))
        lbfgs_list.append((ps, pt, n, c) + acc)
    # averaged perceptron:
    ap_list = []
    for f_name in os.listdir('ap_logs'):
        ps, pt, n, it = f_name.split(".")
        ps = ps[-1]
        pt = pt[-1]
        ps, pt, n, it = map(float, (ps, pt, n, it))
        with open(os.path.join('ap_logs', f_name)) as f:
            acc = optimized_scores(parse_crfsuite_log(f))
        ap_list.append((ps, pt, n, it) + acc)
    # passive agressive
    pa_list = []
    for f_name in os.listdir('pa_logs'):
        rest, it = f_name.rsplit(".", 1)
        ps, pt, n, gamma = rest.split(".", 3)
        ps = ps[-1]
        pt = pt[-1]
        ps, pt, n, gamma, it = map(float, (ps, pt, n, gamma, it))
        with open(os.path.join('pa_logs', f_name)) as f:
            acc = optimized_scores(parse_crfsuite_log(f))
        pa_list.append((ps, pt, n, gamma, it) + acc)
    # arow
    arow_list = []
    for f_name in os.listdir('arow_logs'):
        rest, it = f_name.rsplit(".", 1)
        ps, pt, n, r = rest.split(".", 3)
        ps = ps[-1]
        pt = pt[-1]
        ps, pt, n, r, it = map(float, (ps, pt, n, r, it))
        with open(os.path.join('arow_logs', f_name)) as f:
            acc = optimized_scores(parse_crfsuite_log(f))
        arow_list.append((ps, pt, n, r, it) + acc)

    lbfgs, ap, pa, arow = map(np.array,
                              (lbfgs_list, ap_list, pa_list, arow_list))
