from lib2to3.pgen2.token import OP
from typing import Optional
from datetime import datetime

from flask import request
from pydantic import BaseModel

from app import db
from app.models import Todo
from app.auth import AuthSession
from app.auth import login_required
from app.routes.todo import bp


class EditRequest(BaseModel):
    id: int
    checked: bool
    text: Optional[str]


class EditResponse(BaseModel):
    result: bool
    message: str = ""
    id: int
    checked: bool
    text: str
    checked_at: Optional[datetime]


@bp.patch("")
@login_required
def edit(session: AuthSession):
    ctx = EditRequest(**request.json)
    todo = Todo.query.filter_by(
        id=ctx.id,
        owner=session.user_id
    ).first()

    if todo is None:
        return EditResponse(
            result=False,
            message="등록된 투두가 아닙니다.",
            id=ctx.id
        ).dict(), 404

    if todo.checked != ctx.checked:
        todo.checked = ctx.checked

        if todo.checked:
            todo.checked_at = datetime.now()
        else:
            todo.checked_at = None

    if ctx.text is not None:
        todo.text = ctx.text.strip()[:500]

    db.session.commit()

    return EditResponse(
        result=True,
        id=todo.id,
        checked=todo.checked,
        text=todo.text,
        checked_at=todo.checked_at
    )
