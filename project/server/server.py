from flask import Flask
from flask_restx import Api

from project.setup_db import db
from project.views import directors_ns
from project.views import users_ns
from project.views import movies_ns
from project.views import genres_ns
from project.views import auth_ns


api = Api()


def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    api.init_app(app)

    api.add_namespace(directors_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(users_ns)
    api.add_namespace(movies_ns)
    api.add_namespace(auth_ns)

    return app

