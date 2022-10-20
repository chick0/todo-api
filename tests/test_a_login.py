from secrets import token_hex
from datetime import datetime
from hashlib import sha512

from werkzeug.test import TestResponse

from app import db
from app.models import User

from .flag import set_flag

TEST_EMAIL = "chick_0@to-do.kr"
TEST_PASSWORD = token_hex(16)
TEST_HASHED_PASSWORD = sha512(TEST_PASSWORD.encode("utf-8")).hexdigest()
TEST_CREATED_AT = datetime.now()
TEST_LASTLOGIN = None


def test_login(app, client):
    # Test user sign-up
    with app.app_context():
        user = User()
        user.email = TEST_EMAIL
        user.password = TEST_HASHED_PASSWORD
        user.created_at = TEST_CREATED_AT
        user.lastlogin = TEST_LASTLOGIN

        # Skip! E-Mail verify on sign up
        user.email_verified = True

        db.session.add(user)
        db.session.commit()

        # Test user id must be 1
        assert user.id == 1

    response: TestResponse = client.post(
        "/api/login",
        json=dict(
            email=TEST_EMAIL,
            password=TEST_PASSWORD
        )
    )

    assert response.status_code == 201

    set_flag("auth_token", response.json['token'])
