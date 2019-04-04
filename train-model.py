import sys, os
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split, GridSearchCV

# import pickle

from joblib import dump

open_file = open("./combinedData/open_samples.csv")
close_file = open("./combinedData/close_samples.csv")

# get the data and labels
data = []
labels = []

open_samples = open_file.readlines()
for line in open_samples:
    row = map(float, line.split(","))
    data.append(row)
    labels.append(1)

close_samples = close_file.readlines()
for line in close_samples:
    row = map(float, line.split(","))
    data.append(row)
    labels.append(0)

# plt.plot_data(data, labels)

# Create a linear SVM classifier
clf = svm.SVC(kernel='linear')

# Train classifier
clf.fit(data, labels)

dump(clf, 'trained_model.joblib')

print(clf.predict([[7,7,8,8,7,7,7,7,7,7]]))

# Plot decision function on training and test data
# plot_decision_function(X_train, y_train, X_test, y_test, clf)

# Make predictions on unseen test data
# clf_predictions = clf.predict(X_test)
# print("Accuracy: {}%".format(clf.score(X_test, y_test) * 100 ))
