import numpy as np
import matplotlib.pyplot as plt

predict_pl = np.load("predict_pl.npy")
predict_sg = np.load("predict_sg.npy")
scores_sg = np.load("scores_sg.npy")
scores_pl = np.load("scores_pl.npy")

labels = []
labels.append([[], []])
labels.append([[], []])
labels[0][0] = "Binarized with suffix"
labels[0][0] = "Binarized w/o suffix"
labels[1][0] = "Binarized w/ suffix"
labels[1][1] = "Frequency w/ suffix"
labels[0][1] = "Frequency w/o suffix"


def plot_scores(scores):
    marker = ['o', 's']
    line = ['-.', '-']
    plt.xlabel("maximum n-gram size")
    plt.ylabel("correct classification rate")
    plt.xticks((2, 3, 4, 5, 6))
    for i in (0, 1):
        for j in (0, 1):
            plt.plot([2, 3, 4, 5, 6], scores[:, i, j], marker[i] + line[j], label=labels[i][j])


plt.figure(figsize=(15, 6))
plt.subplot(1, 2, 1)
plt.title("Singular model selection")
plot_scores(scores_sg)
plt.legend(loc=4)
plt.subplot(1, 2, 2)
plt.title("Plural model selection")
plot_scores(scores_pl)
plt.show()

plt.figure(figsize=(15, 6))
plt.subplot(1, 2, 1)
plt.title("Singular prediction")
plot_scores(predict_sg)
plt.legend(loc=4)
plt.subplot(1, 2, 2)
plt.title("Plural prediction")
plot_scores(predict_pl)
plt.show()
