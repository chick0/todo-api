from typing import Optional
from datetime import datetime

from flask import request
from pydantic import BaseModel

from app import db
from app.models import Todo
from app.auth import AuthSession
from app.auth import login_required
from app.routes.todo import bp
from app.todo import TodoResponse
from app.utils import timestamp


class CreateRequest(BaseModel):
    text: str


class CreateResponse(BaseModel):
    status: bool
    message: str = ""
    todo: Optional[TodoResponse] = None


@bp.post("")
@login_required
def create(session: AuthSession):
    ctx = CreateRequest(**request.json)

    todo = Todo()
    todo.owner = session.user_id
    todo.checked = False
    todo.text = ctx.text.strip()[:500]

    if len(todo.text) == 0:
        return CreateResponse(
            status=False,
            message="공백은 저장 할 수 없습니다."
        ).dict(), 400

    todo.created_at = datetime.now()
    todo.checked_at = None

    db.session.add(todo)
    db.session.commit()

    return CreateResponse(
        status=True,
        todo=TodoResponse(
            id=todo.id,
            checked=todo.checked,
            text=todo.text,
            created_at=timestamp(todo.created_at),
            checked_at=timestamp(todo.checked_at)
        )
    ).dict(), 201
