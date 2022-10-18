from werkzeug.test import TestResponse

from .flag import get_flag


def test_user_status(client):
    auth_token = get_flag("auth_token")

    response: TestResponse = client.get(
        "/api/user",
        headers={
            "x-auth": auth_token
        }
    )

    assert response.status_code == 200


def test_user_status_more(client):
    auth_token = get_flag("auth_token")

    response: TestResponse = client.get(
        "/api/user/more",
        query_string={
            "cursor": 1
        },
        headers={
            "x-auth": auth_token
        }
    )

    assert response.status_code == 200

    response: TestResponse = client.get(
        "/api/user/more",
        query_string={
            "cursor": "1"
        },
        headers={
            "x-auth": auth_token
        }
    )

    assert response.status_code == 200


def test_user_status_more_cursor_none(client):
    auth_token = get_flag("auth_token")

    response: TestResponse = client.get(
        "/api/user/more",
        query_string={
            "cursor": None
        },
        headers={
            "x-auth": auth_token
        }
    )

    assert response.status_code == 400


def test_user_status_more_cursor_string(client):
    auth_token = get_flag("auth_token")

    response: TestResponse = client.get(
        "/api/user/more",
        query_string={
            "cursor": "abcd"
        },
        headers={
            "x-auth": auth_token
        }
    )

    assert response.status_code == 400
