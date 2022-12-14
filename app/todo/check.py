from typing import Optional
from datetime import datetime

from flask import request
from app.routes.todo import bp
from pydantic import BaseModel

from app import db
from app.models import Todo
from app.auth import AuthSession
from app.auth import login_required
from app.error import APIError
from app.response import BaseResponse
from app.utils import timestamp


class CheckRequest(BaseModel):
    id: int
    checked: bool


class CheckResponse(BaseResponse):
    checked: bool
    checked_at: Optional[int]


@bp.post("/check")
@login_required
def check(session: AuthSession):
    ctx = CheckRequest(**request.json)
    todo = Todo.query.filter_by(
        id=ctx.id,
        owner=session.user_id
    ).first()

    if todo is None:
        raise APIError(
            code=404,
            message="등록된 투두가 아닙니다."
        )

    todo.checked = ctx.checked

    if todo.checked:
        todo.checked_at = datetime.now()
    else:
        todo.checked_at = None

    db.session.commit()

    return CheckResponse(
        checked=todo.checked,
        checked_at=timestamp(todo.checked_at)
    ).dict(), 201
