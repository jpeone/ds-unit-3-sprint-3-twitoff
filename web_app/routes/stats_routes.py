from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

from flask import Blueprint, jsonify, request, flash, redirect

stats_routes = Blueprint('stats_routes', __name__)

# TODO accept some inputs related to the iris training data( x values)
@stats_routes.route('/iris')
def iris():
    X, y = load_iris(return_X_y = True)
    clf = LogisticRegression(random_state = 42, solver = 'lbfgs', multi_class = 'multinomial')
    clf.fit(X, y)
    result = str(clf.predict(X[:2, :]))
    return result # todo return as Json