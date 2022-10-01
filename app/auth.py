from functools import wraps
from datetime import datetime
from datetime import timedelta

from flask import request
from pydantic import BaseModel

from app import db
from app.models import User
from app.models import History
from app.models import DBSession
from app.models import Pin
from app.models import Country
from app.error import APIError
from app.token import create_token as ct
from app.token import parse_token as pt
from app.utils import get_ip
from app.utils import get_help_mail
from geoip import search

name = "auth:token"
token_ttl = timedelta(hours=3)


class AuthToken(BaseModel):
    sid: int
    email: str
    exp: int


class AuthSession(BaseModel):
    sid: int
    user_id: int
    email: str


def parse_token(token: str) -> AuthToken:
    return AuthToken(**pt(token, name))


def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("x-auth", "")
        payload = parse_token(token)

        user: User = User.query.filter_by(
            email=payload.email
        ).first()

        if user is None:
            raise APIError(
                code=400,
                message="등록된 계정이 아닙니다.",
                logout_required=True
            )

        dbs = DBSession.query.filter_by(
            id=payload.sid,
            owner=user.id,
        ).filter(
            DBSession.dropped_at >= datetime.now()
        ).first()

        if dbs is None:
            raise APIError(
                code=401,
                message="인증 세션이 만료되었습니다.",
                logout_required=True
            )

        dbs.last_access = datetime.now()
        db.session.commit()

        kwargs['session'] = AuthSession(
            sid=payload.sid,
            user_id=user.id,
            email=payload.email,
        )

        return f(*args, **kwargs)

    return decorator


def create_auth_token(user: User, pin: Pin = None) -> str:
    allowed_country_code_list = [
        x.code
        for x in Country.query.filter_by(
            owner=user.id
        ).with_entities(
            Country.code
        ).all()
    ]

    if len(allowed_country_code_list) != 0:
        code = search(ip=get_ip()).code
        if code not in allowed_country_code_list:
            raise APIError(
                code=403,
                message="해당 국가에서는 로그인 할 수 없습니다.\n"
                f"(로그인 허용 국가 설정이 잘못되었다면 {get_help_mail()!r}로 메일을 보내주세요.)"
            )

    MAX_DB_SESSION = 5

    if DBSession.query.filter_by(
        owner=user.id
    ).filter(
        DBSession.dropped_at >= datetime.now()
    ).count() >= MAX_DB_SESSION:
        last_accessed_session = DBSession.query.filter_by(
            owner=user.id
        ).filter(
            DBSession.dropped_at >= datetime.now()
        ).order_by(
            DBSession.last_access.asc()
        ).first()

        db.session.delete(last_accessed_session)
        db.session.commit()

    now = datetime.now()
    user.lastlogin = now

    if pin is not None:
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
    dbs.dropped_at = now + token_ttl
    dbs.last_access = None

    db.session.add(dbs)
    db.session.commit()

    payload = AuthToken(
        sid=dbs.id,
        email=user.email,
        exp=int(dbs.dropped_at.timestamp()),
    ).dict()

    return ct(payload, name)
