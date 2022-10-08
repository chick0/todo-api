from flask import request
from app.routes.todo import bp
from pydantic import BaseModel

from app import db
from app.models import Todo
from app.auth import AuthSession
from app.auth import login_required
from app.error import APIError
from app.response import BaseResponse


class DeleteRequest(BaseModel):
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
        raise APIError(
            code=404,
            message="등록된 할 일이 아닙니다."
        )

    db.session.commit()

    return BaseResponse().dict()
