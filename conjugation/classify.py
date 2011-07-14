import sys
from preprocess import get_clf, load_data

if len(sys.argv) < 2:
    filename = 'inf-ez-labeled.txt'
else:
    filename = sys.argv[1]

X, y = load_data(filename)

clf = get_clf(n=5)
clf.fit(X, y)
print clf.score(X, y)