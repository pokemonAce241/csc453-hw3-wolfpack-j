from joblib import load
clf = load('trained_model.joblib')
print(clf.predict([[-9.27,-25.625,-26.7815625,-22.13,-19.5975,-10.2765625,-9.59,-12.63,-11.282499999999999,-9.35]]))
