from datetime import datetime
from datetime import timedelta
from functools import wraps

from flask import request
from pydantic import BaseModel

from app.models import User
from app.error import APIError
from app.token import create_token as ct
from app.token import parse_token as pt

name = "auth:token"


class AuthToken(BaseModel):
    email: str
    exp: int


class AuthSession(BaseModel):
    user_id: int
    email: str


def create_token(email: str) -> str:
    payload = AuthToken(
        email=email,
        exp=int((datetime.now() + timedelta(hours=3)).timestamp())
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
                message="등록된 계정이 아닙니다."
            )

        kwargs['session'] = AuthSession(
            user_id=user.id,
            email=payload.email,
        )

        return f(*args, **kwargs)
    
    return decorator
