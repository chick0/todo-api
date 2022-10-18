from werkzeug.test import TestResponse

from app.models import DBSession

from .flag import get_flag


def test_logout(app, client):
    auth_token = get_flag("auth_token")

    response: TestResponse = client.delete(
        "/api/logout",
        headers={
            "x-auth": auth_token
        }
    )

    assert response.status_code == 200

    with app.app_context():
        dbs = DBSession.query.filter_by(
            owner=1
        ).all()

        # 1. test_b_login:test_login
        # 2. test_b_pin  :test_login_with_pin
        assert len(dbs) == 1
