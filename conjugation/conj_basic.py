# -*- coding: utf-8 -*-
"""
Runs some simple unsupervised visualisation tricks
on the corpus of romanian infinitives. For now, we
do PCA and NMF, with different settings.

Created on Tue Apr 12 19:02:07 2011

Largest values in the first PC correspond to:
0 ţi
1 ţo
2 mă
3 alo
4 rev
5 ţa
6 ţe
7 eja
8 esc
9 reu
10 sju
@author: vene
"""

import numpy as np
from itertools import cycle
import matplotlib.pyplot as pl

from scikits.learn.cluster import AffinityPropagation
from scikits.learn.decomposition import RandomizedPCA, NMF
from scikits.learn.cluster import KMeans
from scikits.learn.neighbors import NeighborsClassifier

from preprocess import extract_features

def plot_projection(model, infinitives, title):
    fig = pl.figure()
    # Binary model: n-gram appears or not
    for i in range(1, 4):  # n-gram length (1 to 3)    
        pl.subplot(2, 3, i)
        data, _ = extract_features(infinitives, i, False)
        projected_data = model.fit(data).transform(data)
        pl.scatter(projected_data[:, 0], projected_data[:, 1])
        pl.title('Binary %d-grams' % i)
    # Frequency model: count the occurences
    for i in range(1, 4):
        pl.subplot(2, 3, 3 + i)
        data, _ = extract_features(infinitives, i, True)
        projected_data = model.fit(data).transform(data)
        pl.scatter(projected_data[:, 0], projected_data[:, 1])
        pl.title('Count %d-grams' % i)
    fig.text(.5, .95, title, horizontalalignment='center')
    pl.figlegend()
    pl.show()


def k_clusters(k, infinitives):
    data, _ = extract_features(infinitives, 3, False)
    kmeans = KMeans(k=k).fit(data)
    print kmeans.inertia_
    nn = NeighborsClassifier(1).fit(data, np.zeros(data.shape[0]))
    _, idx = nn.kneighbors(kmeans.cluster_centers_)
    for inf in infinitives[idx.flatten()]:
        print inf

def affinity(infinitives):
    print "Extracting features..."
    X, _ = extract_features(infinitives, 3, False)
    X_norms = np.sum(X * X, axis=1)
    S = -X_norms[:, np.newaxis] - X_norms[np.newaxis, :] + 2 * np.dot(X, X.T)
    p = 10 * np.median(S)
    print "Fitting affinity propagation clustering..."
    af = AffinityPropagation().fit(S, p)
    indices = af.cluster_centers_indices_
    for i, idx in enumerate(indices):
        print i, infinitives[idx]

    n_clusters_ = len(indices)


    print "Fitting PCA..."
    X = RandomizedPCA(2).fit(X).transform(X)    
    
    print "Plotting..."
    pl.figure(1)
    pl.clf()
    
    colors = cycle('bgrcmyk')
    for k, col in zip(range(n_clusters_), colors):
        class_members = af.labels_ == k
        cluster_center = X[indices[k]]
        pl.plot(X[class_members,0], X[class_members,1], col+'.')
        pl.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                                         markeredgecolor='k', markersize=14)
        for x in X[class_members]:
            pl.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col) 

    pl.title('Estimated number of clusters: %d' % n_clusters_)
    pl.show()

if __name__ == '__main__':
    with open('infinitives.txt') as f:
        infinitives = np.array([unicode(inf) for inf in f])
    ta = False
    if ta:   
        ends_in_ta = np.array([inf.endswith('ta\n') for inf in infinitives])
        infinitives = infinitives[ends_in_ta]

    affinity(infinitives[:2000])    
#    plot_projection(RandomizedPCA(n_components=2), infinitives, 
#                    "PCA projection of %s$ infinitives" % ("-ta" if ta else ""))
#    plot_projection(NMF(n_components=2, tol=0.01, init="nndsvda"), infinitives, 
#                    "NMF projection of %s$ infinitives" % ("-ta" if ta else ""))
#    k_clusters(10, infinitives)
#    print infinitives[0]
#    data, vect = extract_features(infinitives, 2, True)
#    print vect.vocabulary.keys()
#    for token, idx in vect.vocabulary.items():
#        if idx in data[0].nonzero()[0]:
#            print token
