from werkzeug.test import TestResponse

from .flag import set_flag
from .flag import get_flag

path = "/api/pin"
path_login = path + "/login"


def test_create_pin(client):
    auth_token = get_flag("auth_token")

    response: TestResponse = client.post(
        path,
        headers={
            "x-auth": auth_token
        },
        json={
            "code": "123456"
        }
    )

    assert response.status_code == 201

    set_flag("pin_token", response.json['token'])


def test_login_with_pin_fail_wrong_code(client):
    pin_token = get_flag("pin_token")

    response: TestResponse = client.post(
        path_login,
        headers={
            "x-pin": pin_token
        },
        json={
            "code": "654321"
        }
    )

    assert response.status_code == 400


def test_login_with_pin(client):
    pin_token = get_flag("pin_token")

    response: TestResponse = client.post(
        path_login,
        headers={
            "x-pin": pin_token
        },
        json={
            "code": "123456"
        }
    )

    assert response.status_code == 201

    set_flag("auth_by_pin", response.json['token'])


def test_delete_pin(client):
    auth_token = get_flag("auth_token")

    response: TestResponse = client.delete(
        path,
        headers={
            "x-auth": auth_token
        },
        json={
            "id": 1
        }
    )

    assert response.status_code == 200


def test_login_with_pin_fail_deleted_pin(client):
    pin_token = get_flag("pin_token")

    response: TestResponse = client.post(
        path_login,
        headers={
            "x-pin": pin_token
        },
        json={
            "code": "123456"
        }
    )

    assert response.status_code == 404
