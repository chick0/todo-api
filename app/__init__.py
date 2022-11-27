from os import environ
from logging import getLogger
from datetime import datetime
from importlib import import_module

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from redis import Redis
from pydantic.error_wrappers import ValidationError

from git import get_commit_id

db = SQLAlchemy()
migrate = Migrate()
logger = getLogger()


def create_app():
    app = Flask(__name__, static_folder=None)
    app.config['SQLALCHEMY_DATABASE_URI'] = environ['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['algorithms'] = [
        "HS256",
    ]

    app.config['VERSION'] = {
        "started_at": datetime.now().timestamp(),
        "commit": get_commit_id()
    }

    app.config['redis'] = Redis.from_url(environ['REDIS_URL'])

    import_module("app.models")
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

    from app import routes
    for route in [getattr(routes, name) for name in routes.__all__]:
        app.register_blueprint(blueprint=route.bp)

    # error handler
    from app.error import APIError
    from app.error import handle_api_error
    from app.error import validation_error
    from app.error import not_found_error

    app.register_error_handler(
        code_or_exception=APIError,
        f=handle_api_error
    )

    app.register_error_handler(
        code_or_exception=ValidationError,
        f=validation_error
    )

    app.register_error_handler(
        code_or_exception=404,
        f=not_found_error
    )

    return app
