from typing import Optional

from flask import request
from app.routes.todo import bp
from pydantic import BaseModel

from app import db
from app.models import Todo
from app.auth import AuthSession
from app.auth import login_required
from app.error import APIError
from app.response import BaseResponse


class EditRequest(BaseModel):
    id: int
    text: str


class EditResponse(BaseResponse):
    text: Optional[str]


@bp.patch("")
@login_required
def edit(session: AuthSession):
    ctx = EditRequest(**request.json)
    todo = Todo.query.filter_by(
        id=ctx.id,
        owner=session.user_id
    ).first()

    if todo is None:
        raise APIError(
            code=404,
            message="등록된 투두가 아닙니다."
        )

    todo.text = ctx.text.strip()[:500]

    if len(todo.text) == 0:
        return EditResponse(
            status=False,
            message="할 일이 삭제되었습니다.",
        ).dict()

    db.session.commit()

    return EditResponse(
        text=todo.text,
    ).dict(), 201
