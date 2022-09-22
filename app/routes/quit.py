from typing import Optional
from hashlib import sha512

from flask import Blueprint
from flask import request
from pydantic import BaseModel

from app import db
from app.models import User
from app.models import Todo
from app.models import History
from app.models import DBSession
from app.auth import AuthSession
from app.auth import login_required
from app.quit import create_token
from app.quit import check_quit_session

bp = Blueprint("quit", __name__, url_prefix="/api/quit")


class CheckPasswordRequest(BaseModel):
    password: str


class QuitResponse(BaseModel):
    status: bool
    message: str
    token: Optional[str]


@bp.post("")
@login_required
def check_password(session: AuthSession):
    ctx = CheckPasswordRequest(**request.json)
    ctx.password = sha512(ctx.password.encode()).hexdigest()

    user: User = User.query.filter_by(
        id=session.user_id,
        email=session.email,
        password=ctx.password
    ).first()

    if user is None:
        return QuitResponse(
            status=False,
            message="비밀번호가 일치하지 않습니다."
        ).dict(), 400

    return QuitResponse(
        status=True,
        message="비밀번호가 일치합니다.",
        token=create_token(
            user_id=session.user_id
        )
    ).dict(), 201


@bp.delete("")
@login_required
@check_quit_session
def quit(session: AuthSession):
    DBSession.query.filter_by(
        owner=session.user_id
    ).delete()

    History.query.filter_by(
        owner=session.user_id
    ).delete()

    Todo.query.filter_by(
        owner=session.user_id
    ).delete()

    User.query.filter_by(
        id=session.user_id
    ).delete()

    db.session.commit()

    return QuitResponse(
        status=True,
        message="계정이 삭제되었습니다."
    ).dict()
