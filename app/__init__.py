from os import environ
from os.path import join
from os.path import abspath
from os.path import dirname
from logging import getLogger
from datetime import datetime
from importlib import import_module

from flask import Flask
from flask import Response
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from redis import Redis
from pydantic.error_wrappers import ValidationError
from werkzeug.exceptions import NotFound

db = SQLAlchemy()
migrate = Migrate()
logger = getLogger()


def create_app():
    app = Flask(__name__, static_folder=None)
    app.config['SQLALCHEMY_DATABASE_URI'] = environ['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.algorithms = [
        "HS256",
    ]

    try:
        from flask_cors import CORS

        CORS(
            app,
            resources={
                r"/api/*": dict(
                    origins="*",
                    send_wildcard=False,
                    methods=[
                        "OPTIONS",
                        "GET",
                        "POST",
                        "PATCH",
                        "DELETE"
                    ],
                    allow_headers=[
                        "User-Agent",
                        "Content-Type",
                        "x-auth",
                        "x-quit",
                        "x-reset"
                    ]
                )
            }
        )

        logger.info("CORS is enabled")
    except ImportError:
        logger.info("CORS is disabled")

    import_module("app.models")
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

    app.redis = Redis.from_url(environ['REDIS_URL'])

    BASE_DIR = dirname(dirname(abspath(__file__)))
    DIST_DIR = join(BASE_DIR, "dist")

    def not_found_error(error):
        try:
            return send_from_directory(
                directory=DIST_DIR,
                path="404.html"
            ), 404
        except NotFound:
            return {
                "status": False,
                "message": "Not Found"
            }, 404

    @app.get("/")
    @app.get("/<path:path>")
    def frontend(path = None):  # noqa: E251
        if path is None:
            path = "index.html"

        try:
            response: Response = send_from_directory(
                directory=DIST_DIR,
                path=path
            )
        except NotFound:
            return not_found_error(None)

        if path.endswith(".js"):
            response.content_type = "text/javascript; charset=utf-8"

        return response

    from app import routes
    for route in [getattr(routes, name) for name in routes.__all__]:
        app.register_blueprint(blueprint=route.bp)

    # error handler
    from app.error import APIError
    from app.error import handle_api_error
    from app.error import validation_error

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

    try:
        target = "ref:"
        path = None

        with open(join(".git", "HEAD"), mode="r") as head_reader:
            for data in head_reader.read().split("\n"):
                if data.startswith(target):
                    result = data[len(target):].strip()
                    path = join(".git", result)

        if path is None:
            raise FileNotFoundError

        with open(path, mode="r") as commit_reader:
            commit_hash = commit_reader.read()[:7]
    except FileNotFoundError:
        commit_hash = "-------"

    app.commit_hash = commit_hash
    app.started_at = datetime.now()
    return app
