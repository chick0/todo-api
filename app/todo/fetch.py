from pydantic import BaseModel

from app.models import Todo

from app.auth import AuthSession
from app.auth import login_required
from app.routes.todo import bp
from app.todo import TodoResponse
from app.todo import timestamp


class TodoListResponse(BaseModel):
    result: bool
    message: str = ""
    todos: list[TodoResponse]


@bp.get("")
@login_required
def fetch(session: AuthSession):
    todos = Todo.query.filter_by(
        owner=session.user_id
    ).order_by(
        Todo.checked.desc()
    ).order_by(
        Todo.created_at.desc()
    ).limit(100).all()

    return TodoListResponse(
        result=True,
        todos=[
            TodoResponse(
                id=x.id,
                checked=x.checked,
                text=x.text,
                created_at=timestamp(x.created_at),
                checked_at=timestamp(x.checked_at)
            )
            for x in todos
        ]
    ).dict()
