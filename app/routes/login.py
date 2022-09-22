from hashlib import sha512
from datetime import datetime
from datetime import timedelta

from flask import Blueprint
from flask import request
from pydantic import BaseModel

from app import db
from app.models import User
from app.models import History
from app.models import DBSession
from app.utils import get_ip
from app.auth import create_token

bp = Blueprint("login", __name__, url_prefix="/api/login")


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    status: bool
    message: str = ""
    token: str = ""
    email_verify_required: bool = False


@bp.post("")
def email_and_password():
    ctx = LoginRequest(**request.json)
    ctx.password = sha512(ctx.password.encode("utf-8")).hexdigest()

    user: User = User.query.filter_by(
        email=ctx.email,
        password=ctx.password
    ).first()

    if user is None:
        return LoginResponse(
            status=False,
            message="등록된 계정이 아닙니다."
        ).dict(), 404

    if not user.email_verified:
        return LoginResponse(
            status=False,
            message="이메일 인증이 완료되지 않은 계정은 사용 할 수 없습니다.",
            email_verify_required=True
        ).dict(), 400

    now = datetime.now()
    user.lastlogin = now

    history = History()
    history.owner = user.id,
    history.created_at = now
    history.ip = get_ip()
    history.user_agent = str(request.user_agent).strip()[:500]

    db.session.add(history)
    db.session.commit()

    dbs = DBSession()
    dbs.owner = user.id
    dbs.history = history.id
    dbs.dropped_at = datetime.now() + timedelta(hours=3)
    dbs.last_access = datetime.now()

    db.session.add(dbs)
    db.session.commit()

    return LoginResponse(
        status=True,
        token=create_token(
            session_id=dbs.id,
            email=user.email,
            exp=dbs.dropped_at
        )
    ).dict()
