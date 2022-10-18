from os import urandom
from werkzeug.test import TestResponse

from app.models import Notice

from .flag import get_flag


def test_notice_create_success(app, client):
    auth_token = get_flag("auth_token")

    rand_string = urandom(4).hex()

    title = "title_" + rand_string
    text = "text_" + rand_string

    response: TestResponse = client.post(
        "/api/notice",
        headers={
            "x-auth": auth_token
        },
        json=dict(
            title=title,
            text=text
        )
    )

    assert response.status_code == 201

    with app.app_context():
        nts = Notice.query.all()

        assert len(nts) == 1

        nt: Notice = nts[0]

        assert nt.title == title and nt.text == text
