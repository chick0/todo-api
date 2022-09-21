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
from app.todo import timestamp


class CreateRequest(BaseModel):
    text: str


class CreateResponse(BaseModel):
    result: bool
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

    todo.created_at = datetime.now()
    todo.checked_at = None

    db.session.add(todo)
    db.session.commit()

    return CreateResponse(
        result=True,
        todo=TodoResponse(
            id=todo.id,
            checked=todo.checked,
            text=todo.text,
            created_at=timestamp(todo.created_at),
            checked_at=timestamp(todo.checked_at)
        )
    ).dict(), 201
