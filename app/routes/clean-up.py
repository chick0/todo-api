from flask import Blueprint

from app import db
from app.models import Todo
from app.auth import AuthSession
from app.auth import login_required
from app.todo import MAX_TODO
from app.response import BaseResponse

bp = Blueprint("clean-up", __name__, url_prefix="/api/clean-up")


class StatusResponse(BaseResponse):
    max: int = MAX_TODO
    total: int
    checked: int


@bp.get("")
@login_required
def status(session: AuthSession):
    return StatusResponse(
        total=Todo.query.filter_by(
            owner=session.user_id
        ).count(),
        checked=Todo.query.filter_by(
            owner=session.user_id,
            checked=True
        ).count()
    ).dict()


@bp.delete("")
@login_required
def delete(session: AuthSession):
    Todo.query.filter_by(
        owner=session.user_id,
        checked=True
    ).delete()

    db.session.commit()
    return BaseResponse().dict()
