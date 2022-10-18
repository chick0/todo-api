from werkzeug.test import TestResponse

from app import db
from app.models import User
from app.models import Admin

from .flag import set_flag
from .flag import get_flag
from .test_a_login import TEST_PASSWORD

path = "/api/quit"


def test_quit_step_1(client):
    auth_token = get_flag("auth_by_pin")

    response: TestResponse = client.post(
        path,
        headers={
            "x-auth": auth_token
        },
        json={
            "password": TEST_PASSWORD
        }
    )

    assert response.status_code == 201
    set_flag("quit_token", response.json['token'])


def test_quit_step_2_fail(client):
    auth_token = get_flag("auth_by_pin")
    quit_token = get_flag("quit_token")

    response: TestResponse = client.delete(
        path,
        headers={
            "x-auth": auth_token,
            "x-quit": quit_token
        }
    )

    assert response.status_code == 400


def test_quit_step_2(app, client):
    with app.app_context():
        Admin.query.filter_by(
            user=1
        ).delete()

        db.session.commit()

    auth_token = get_flag("auth_by_pin")
    quit_token = get_flag("quit_token")

    response: TestResponse = client.delete(
        path,
        headers={
            "x-auth": auth_token,
            "x-quit": quit_token
        }
    )

    assert response.status_code == 200

    with app.app_context():
        test_user = User.query.filter_by(
            id=1
        ).first()

        assert test_user is None
