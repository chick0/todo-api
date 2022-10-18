from werkzeug.test import TestResponse

from .flag import get_flag


def test_notice_create_fail(client):
    auth_token = get_flag("auth_token")

    response: TestResponse = client.post(
        "/api/notice",
        headers={
            "x-auth": auth_token
        },
        json=dict(
            title="title",
            text="text"
        )
    )

    assert response.status_code == 403
