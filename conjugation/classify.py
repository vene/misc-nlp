import sys
from scikits.learn.linear_model.sparse import LogisticRegression
from preprocess import get_clf, load_data

if len(sys.argv) < 2:
    filename = 'inf-esc-labeled.txt'
else:
    filename = sys.argv[1]

X, y = load_data(filename)

clf = get_clf(n=3, clf=LogisticRegression())
clf.fit(X, y)
print clf.score(X, y)