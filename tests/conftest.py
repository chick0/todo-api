import pytest
from dotenv import load_dotenv

from app import db
from app import create_app

from . import DATABASE_DIR


@pytest.fixture
def app():
    load_dotenv()
    app = create_app()

    # Setup test database
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_DIR

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
