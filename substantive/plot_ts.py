def plot(scores, scores2=None):
    import matplotlib.pylab as pl
    from matplotlib.ticker import FuncFormatter

    def percentages(x, pos=0):
        return '%2.2f%%' % (100 * x)

    def percentages2(x, pos=0):
        return '%2.0f%%' % (100 * x)

    pl.figure(figsize=(12, 5))
    ax1 = pl.subplot(121)
    pl.errorbar(scores2[:, 1], scores2[:, 2], yerr=scores2[:, 5],
                c='k', marker='o')
    pl.xlim([0.08, 1.02])
    #if scores2 is not None:
    #    pl.errorbar(scores2[:, 1] + 0.02, scores2[:, 2], yerr=scores2[:, 5],
    #            c='0.5', marker='s')
    pl.title("Singular")
    ax1.yaxis.set_major_formatter(FuncFormatter(percentages))

    ax2 = pl.subplot(122, sharex=ax1)
    pl.errorbar(scores[:, 1], scores[:, 3], yerr=scores[:, 6],
                c='k', marker='o')
    if scores2 is not None:
        pl.errorbar(scores2[:, 1], scores2[:, 3], yerr=scores2[:, 6],
                c='k', marker='s')

    ax2.yaxis.set_major_formatter(FuncFormatter(percentages2))

    #ax3 = pl.subplot(313, sharex=ax2)
    pl.errorbar(scores[:, 1] + 0.02, scores[:, 4], yerr=scores[:, 7],
                c='0.5', marker='o')
    if scores2 is not None:
        pl.errorbar(scores2[:, 1] + 0.02, scores2[:, 4], yerr=scores2[:, 7],
                c='0.5', marker='s')
    pl.xlim([0.08, 1.04])
    pl.title("Plural and combined")
    pl.ylabel("Accuracy")
    #ax3.yaxis.set_major_formatter(FuncFormatter(percentages))
    #pl.setp(ax3.get_xticklabels(), visible=False)
    pl.suptitle('Proportion of training set used', y=0.05, fontsize=12)
    pl.subplots_adjust(.07, .1, .98, .9, .15, .2)
    #pl.show()

    for ext in ('pdf', 'svg', 'png'):
        pl.savefig('train_size-i.%s' % ext)


import numpy as np

scores = np.load("train_size.npy")
scores2 = np.load("train_size_i.npy")

plot(scores2, scores)
