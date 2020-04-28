from flask import Flask
import os

from web_app.models import db, migrate
from web_app.routes.home_routes import home_routes
from web_app.routes.book_routes import book_routes
from web_app.routes.twitter_routes import twitter_routes
from web_app.routes.admin_routes import admin_routes
from web_app.routes.stats_routes import stats_routes

#couldn't get this to work with absolute or os generated file path
DATABASE_URI = "sqlite:///development.db"

SECRET_KEY = 'super secret'

def create_app():
    app = Flask(__name__)

    print(DATABASE_URI)

    app.config['SECRET_KEY'] = SECRET_KEY #enalbe flash messaging
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home_routes)
    app.register_blueprint(book_routes)
    app.register_blueprint(twitter_routes)
    app.register_blueprint(admin_routes)
    app.register_blueprint(stats_routes)
    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)