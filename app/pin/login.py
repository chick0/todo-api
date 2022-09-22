from cgitb import reset
from hashlib import sha512
from datetime import datetime
from datetime import timedelta

from flask import request
from pydantic import BaseModel

from app.routes.pin import bp
from app import db
from app.models import User
from app.models import History
from app.models import DBSession
from app.models import Pin
from app.error import APIError
from app.pin import parse_token
from app.auth import create_token
from app.utils import get_ip


class PinLoginRequest(BaseModel):
    code: str


class PinLoginResponse(BaseModel):
    status: bool
    message: str = ""
    token: str


@bp.post("/login")
def login():
    ctx = PinLoginRequest(**request.json)
    ctx.code = sha512(ctx.code.encode()).hexdigest()

    token = request.headers.get("x-pin", "")
    payload = parse_token(token=token)

    user: User = User.query.filter_by(
        id=payload.uid,
        email_verified=True
    ).first()

    if user is None:
        raise APIError(
            code=404,
            message="등록된 계정이 아닙니다."
        )

    pin: Pin = Pin.query.filter_by(
        id=payload.pid,
        owner=payload.uid,
        user_agent=str(request.user_agent).strip()[:500]
    ).first()

    if pin is None:
        raise APIError(
            code=403,
            message="등록된 PIN이 아닙니다.",
            logout_required=True
        )

    if pin.code != ctx.code:
        pin.fail_count = Pin.fail_count + 1
        db.session.commit()

        raise APIError(
            code=403,
            message=f"올바르지 않은 PIN을 입력했습니다. (실패 횟수:{pin.fail_count}/5)"
        )

    if pin.fail_count > 5:
        raise APIError(
            code=403,
            message="해당 PIN은 실패 횟수가 많아 차단되었습니다."
        )

    signature = token.split(".")[-1]

    if pin.signature != signature:
        pin.fail_count = Pin.fail_count + 1
        db.session.commit()

        raise APIError(
            code=403,
            message=f"토큰 시그니쳐가 올바르지 않습니다. (실패 횟수:{pin.fail_count}/5)"
        )

    now = datetime.now()
    user.lastlogin = now

    pin.ip = get_ip()
    pin.last_access = now

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

    return PinLoginResponse(
        status=True,
        token=create_token(
            session_id=dbs.id,
            email=user.email,
            exp=dbs.dropped_at
        )
    ).dict()
