import numpy as np

#from sklearn.base import BaseEstimator
#from sklearn.feature_extraction import DictVectorizer
#from sklearn.pipeline import Pipeline
#from sklearn.grid_search import GridSearchCV
#from sklearn.externals import joblib

from pystruct.models import ChainCRF, EdgeTypeGraphCRF
from pystruct.learners import OneSlackSSVM
from pystruct.learners import StructuredPerceptron


class HackSVM(OneSlackSSVM):
    def fit(self, X, Y, constraints=None, warm_start=None):
        model = (self.model if isinstance(self.model, type)
                 else self.model.__class__)
        self.model = model(n_states=34, n_features=X[0].shape[1])
        OneSlackSSVM.fit(self, X, Y, constraints, warm_start)


class HackPerc(StructuredPerceptron):
    def fit(self, X, Y):
        model = (self.model if isinstance(self.model, type)
                 else self.model.__class__)
        self.model = model(n_states=34, n_features=X[0].shape[1])
        StructuredPerceptron.fit(self, X, Y)


class StressCRF(ChainCRF, EdgeTypeGraphCRF):
    """CRF in which each direction of edges has their own set of parameters.

    Pairwise potentials are not symmetric and are independend for each kind of
    edges. This leads to n_classes * n_features parameters for unary potentials
    and n_edge_types * n_classes ** 2 parameters for edge potentials.
    The number of edge-types is two for a 4-connected neighborhood
    (horizontal and vertical) or 4 for a 8 connected neighborhood (additionally
    two diagonals).

    Unary evidence ``x`` is given as array of shape (width, height, n_states),
    labels ``y`` are given as array of shape (width, height). Grid sizes do not
    need to be constant over the dataset.

    Parameters
    ----------
    n_states : int, default=2
        Number of states for all variables.

    inference_method : string, default="qpbo"
        Function to call do do inference and loss-augmented inference.
        Possible values are:

            - 'qpbo' for QPBO + alpha expansion.
            - 'dai' for LibDAI bindings (which has another parameter).
            - 'lp' for Linear Programming relaxation using GLPK.
            - 'ad3' for AD3 dual decomposition.

    neighborhood : int, default=4
        Neighborhood defining connection for each variable in the grid.
        Possible choices are 4 and 8.
    """
    def __init__(self, n_states=2, n_features=None, inference_method='qpbo'):
        ChainCRF.__init__(self, n_states, n_features,
                          inference_method=inference_method)
        self.n_edge_types = 4
        self.size_psi = (n_states * self.n_features
                         + self.n_edge_types * n_states ** 2)

    def get_edges(self, x, flat=True):
        spl, stress = x
        n = spl.shape[0]
        m = stress.shape[0]
        inds_n = np.arange(n)
        inds_m = n + np.arange(m)
        A = np.c_[inds_n[:-1], inds_n[1:]]
        B = np.c_[inds_m[:-1], inds_m[1:]]
        C = np.c_[inds_m[:-1], inds_n]
        D = np.c_[inds_m[1:], inds_n]
        if flat:
            return np.r_[A, B, C, D]
        else:
            return [A, B, C, D]

    def get_features(self, x):
        xa = x[0].toarray()
        xb = x[1].toarray()
        return np.r_[np.c_[xa, np.zeros((xa.shape[0], xb.shape[1]))],
                     np.c_[np.zeros((xb.shape[0], xa.shape[1])), xb]]

    def _reshape_y(self, y, shape_x, return_energy):
        if return_energy:
            y, energy = y

        if isinstance(y, tuple):
            y = (y[0].reshape(2 * shape_x + 1, y[0].shape[1]), y[1])
        else:
            y = y.reshape(2 * shape_x + 1,)  # works for chains too

        if return_energy:
            return y, energy
        return y

    def inference(self, x, w, relaxed=False, return_energy=False):
        y = EdgeTypeGraphCRF.inference(self, x, w, relaxed=relaxed,
                                       return_energy=return_energy)
        return self._reshape_y(y, x[0].shape[0], return_energy)

    def loss_augmented_inference(self, x, y, w, relaxed=False,
                                 return_energy=False):
        y_hat = EdgeTypeGraphCRF.loss_augmented_inference(
            self, x, y.ravel(), w, relaxed=relaxed,
            return_energy=return_energy)
        return self._reshape_y(y_hat, x[0].shape[0], return_energy)


def score(y_true, y_pred):
    word_syl = word_stress = 0
    char_syl = char_stress = 0
    n_items_syl, n_items_stress = 0
    for y_t, y_p in zip(y_true, y_pred):
        midp = int((y_t.shape[0] - 1) / 2)
        corr_syl = y_t[:midp] == y_p[:midp]
        corr_stress = y_t[midp:] == y_p[midp:]
        word_syl += corr_syl.all()
        word_stress += corr_stress.all()
        char_syl += corr_syl.sum()
        char_stress += corr_stress.sum()
        n_items_syl += midp
        n_items_stress += midp + 1
    return (word_syl * 1.0 / len(y_true), word_stress * 1.0 / len(y_true),
            char_syl * 1.0 / n_items_syl, char_stress * 1.0 / n_items_stress)
