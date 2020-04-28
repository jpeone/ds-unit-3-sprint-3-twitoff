from flask import Blueprint, render_template

home_routes = Blueprint('home_routes', __name__)

@home_routes.route('/')
def hello_world():
    print('made it to the main page')
    return render_template('prediction_form.html')

@home_routes.route('/about')
def about():
    return('About me')