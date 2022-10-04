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
from app.models import Pin
from app.auth import AuthSession
from app.auth import login_required
from app.quit import create_token
from app.quit import check_quit_session
from app.error import APIError

bp = Blueprint("quit", __name__, url_prefix="/api/quit")


class CheckPasswordRequest(BaseModel):
    password: str


class QuitResponse(BaseModel):
    status: bool = True
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
        raise APIError(
            code=400,
            message="비밀번호가 일치하지 않습니다."
        )

    return QuitResponse(
        message="비밀번호가 일치합니다.",
        token=create_token(
            user_id=session.user_id
        )
    ).dict(), 201


@bp.delete("")
@login_required
@check_quit_session
def quit(session: AuthSession):
    # 로그인 세선 (디비 세션)
    # - 계정
    # - 로그인 기록
    DBSession.query.filter_by(
        owner=session.user_id
    ).delete()

    # 로그인 기록
    # - 계정
    History.query.filter_by(
        owner=session.user_id
    ).delete()

    # 할 일
    # - 계정
    Todo.query.filter_by(
        owner=session.user_id
    ).delete()

    # PIN
    # - 계정
    Pin.query.filter_by(
        owner=session.user_id
    ).delete()

    # 계정
    User.query.filter_by(
        id=session.user_id
    ).delete()

    db.session.commit()

    return QuitResponse(
        message="계정이 삭제되었습니다."
    ).dict()
