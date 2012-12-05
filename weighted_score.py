import numpy as np
import pandas as pd

GROZEA = '/Users/vene/corpora/grozea/utf8/counts.txt'
NGRAMS = '/Users/vene/corpora/ROMANIAN/1gms/vocab.bz2'


def freq_weights(words, corpus='grozea', corpus_stats=None, strip=False):
    if strip:
        from sklearn.feature_extraction.text import strip_accents_unicode
        words = strip_accents_unicode(words)
    if corpus == 'grozea':
        corpus_stats = pd.read_csv(GROZEA, sep='[  ]',
                                   names=['freq', 'word'], index_col=1)
    elif corpus == 'ngrams':
        import bz2
        corpus_stats = pd.read_csv(bz2.BZ2File(NGRAMS), sep='[\t]',
                                   names=['word', 'freq'])
    w = np.ones(len(words))
    for k, word in enumerate(words):
        try:
            if corpus == 'ngrams':
                w[k] += corpus_stats['freq'][np.where(corpus_stats['word'] == word)[0]]
            else:
                w[k] += corpus_stats.lookup([word], ['freq'])[0]
        except:
            pass
    return w / w.sum()
