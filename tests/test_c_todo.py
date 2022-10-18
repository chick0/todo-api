from werkzeug.test import TestResponse

from app.models import Todo

from .flag import get_flag

path = "/api/todo"

TEST_TODO_CONTENT = "test"
TEST_TODO_EDIT = "test!"


def test_create_todo(client):
    auth_token = get_flag("auth_token")

    response: TestResponse = client.post(
        path,
        headers={
            "x-auth": auth_token
        },
        json={
            "text": TEST_TODO_CONTENT
        }
    )

    assert response.status_code == 201


def test_check_todo(app, client):
    with app.app_context():
        todo = Todo.query.filter_by(
            id=1,
            owner=1,
            checked=False,
            text=TEST_TODO_CONTENT
        ).first()

        assert todo is not None

    auth_token = get_flag("auth_token")

    response: TestResponse = client.post(
        path + "/check",
        headers={
            "x-auth": auth_token
        },
        json={
            "id": 1,
            "checked": True
        }
    )

    assert response.status_code == 201


def test_edit_todo(app, client):
    with app.app_context():
        todo = Todo.query.filter_by(
            id=1,
            owner=1,
            checked=True,
            text=TEST_TODO_CONTENT
        ).first()

        assert todo is not None

    auth_token = get_flag("auth_token")

    response: TestResponse = client.patch(
        path,
        headers={
            "x-auth": auth_token
        },
        json={
            "id": 1,
            "text": TEST_TODO_EDIT
        }
    )

    assert response.status_code == 201

    with app.app_context():
        todo = Todo.query.filter_by(
            id=1,
            owner=1,
            checked=True,
            text=TEST_TODO_EDIT
        ).first()

        assert todo is not None


def test_delete_todo(app, client):
    with app.app_context():
        todo = Todo.query.filter_by(
            id=1,
            owner=1,
            checked=True,
            text=TEST_TODO_EDIT
        ).first()

        assert todo is not None

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
