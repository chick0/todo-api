from datetime import datetime
from datetime import timedelta
from functools import wraps

from flask import request
from pydantic import BaseModel

from app.token import create_token as ct
from app.token import parse_token as pt

name = "auth:token"


class AuthToken(BaseModel):
    email: str
    exp: int


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
        kwargs['session'] = payload
        return f(*args, **kwargs)
    
    return decorator
