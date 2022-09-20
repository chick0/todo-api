from os import environ
from os.path import join
from os.path import abspath
from os.path import dirname
from logging import getLogger
from importlib import import_module

from flask import Flask
from flask import Response
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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
        CORS(app, resources={r"/api/*": {"origins": "*"}})
        logger.info("CORS is enabled")
    except ImportError:
        logger.info("CORS is disabled")

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

    from app import routes
    for route in [getattr(routes, name) for name in routes.__all__]:
        app.register_blueprint(blueprint=route.bp)

    # error handler
    from app.error import VerifyFail
    from app.error import handle_error_with_reason

    app.register_error_handler(
        code_or_exception=VerifyFail,
        f=handle_error_with_reason
    )

    return app
