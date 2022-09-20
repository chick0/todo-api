from os import environ
from os.path import join
from os.path import abspath
from os.path import dirname
from importlib import import_module

from flask import Flask
from flask import Response
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = environ['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    import_module("app.models")
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

    BASE_DIR = dirname(dirname(abspath(__file__)))
    DIST_DIR = join(BASE_DIR, "dist")

    @app.get("/")
    @app.get("/<path:path>")
    def frontend(path = None):
        if path is None:
            path = "index.html"

        response: Response = send_from_directory(
            directory=DIST_DIR,
            path=path
        )

        if path.endswith(".js"):
            response.content_type = "text/javascript; charset=utf-8"

        return response


    @app.get("/api/sudo")
    def sudo():
        return {
            "sudo": False
        }, 404

    return app
