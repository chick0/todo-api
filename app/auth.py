from datetime import datetime
from datetime import timedelta
from functools import wraps

from flask import request
from pydantic import BaseModel

from app.models import User
from app.models import DBSession
from app.error import APIError
from app.token import create_token as ct
from app.token import parse_token as pt

name = "auth:token"


class AuthToken(BaseModel):
    sid: int
    email: str
    exp: int


class AuthSession(BaseModel):
    sid: int
    user_id: int
    email: str


def create_token(session_id: int, email: str, exp: datetime) -> str:
    payload = AuthToken(
        sid=session_id,
        email=email,
        exp=int(exp.timestamp()),
    ).dict()

    return ct(payload, name)


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

        kwargs['session'] = AuthSession(
            sid=payload.sid,
            user_id=user.id,
            email=payload.email,
        )

        return f(*args, **kwargs)
    
    return decorator
