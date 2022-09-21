from flask import request
from pydantic import BaseModel

from app import db
from app.models import Todo
from app.auth import AuthSession
from app.auth import login_required
from app.routes.todo import bp


class EditRequest(BaseModel):
    id: int
    text: str


class EditResponse(BaseModel):
    status: bool
    message: str = ""
    text: str


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
            status=False,
            message="등록된 투두가 아닙니다.",
        ).dict(), 404

    todo.text = ctx.text.strip()[:500]
    db.session.commit()

    return EditResponse(
        status=True,
        text=todo.text,
    ).dict(), 201
