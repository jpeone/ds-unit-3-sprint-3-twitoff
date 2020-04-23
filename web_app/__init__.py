from flask import Flask
import os

from web_app.models import db, migrate
from web_app.routes.home_routes import home_routes
from web_app.routes.book_routes import book_routes

#couldn't get this to work with absolute or os generated file path
DATABASE_URI = "sqlite:///development.db"

def create_app():
    app = Flask(__name__)

    print(DATABASE_URI)

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home_routes)
    app.register_blueprint(book_routes)
    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)