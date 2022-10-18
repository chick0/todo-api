from datetime import datetime

from werkzeug.test import TestResponse

from app import db
from app.models import Admin

from .flag import get_flag


def test_admin(app, client):
    auth_token = get_flag("auth_token")

    response: TestResponse = client.get(
        "/api/admin",
        headers={
            "x-auth": auth_token
        }
    )

    assert response.status_code == 403 and response.json['admin'] is False

    with app.app_context():
        ad = Admin()
        ad.user = 1
        ad.created_at = datetime.now()

        db.session.add(ad)
        db.session.commit()

    response: TestResponse = client.get(
        "/api/admin",
        headers={
            "x-auth": auth_token
        }
    )

    assert response.status_code == 200 and response.json['admin'] is True
