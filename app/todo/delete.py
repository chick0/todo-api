from flask import request
from pydantic import BaseModel

from app import db
from app.models import Todo
from app.auth import AuthSession
from app.auth import login_required
from app.routes.todo import bp


class DeleteRequest(BaseModel):
    id: int


class DeleteResponse(BaseModel):
    status: bool
    message: str = ""
    id: int


@bp.delete("")
@login_required
def delete(session: AuthSession):
    ctx = DeleteRequest(**request.json)
    todo = Todo.query.filter_by(
        id=ctx.id,
        owner=session.user_id
    ).delete()

    if todo == 0:
        return DeleteResponse(
            status=False,
            message="등록된 투두가 아닙니다.",
            id=ctx.id
        ).dict(), 404

    db.session.commit()

    return DeleteResponse(
        status=True,
        id=ctx.id
    ).dict()
