from datetime import datetime
from datetime import timedelta
from functools import wraps

from flask import request
from pydantic import BaseModel

from app.auth import APIError
from app.token import create_token as ct
from app.token import parse_token as pt

name = "verify:quit"


class QuitSession(BaseModel):
    uid: int
    exp: int


def create_token(user_id: int) -> str:
    return ct(
        payload=QuitSession(
            uid=user_id,
            exp=int((datetime.now() + timedelta(minutes=5)).timestamp())
        ).dict(),
        name=name
    )


def parse_token(token: str) -> QuitSession:
    return QuitSession(**pt(token, name))


def check_quit_session(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("x-quit", "")
        payload: QuitSession = parse_token(token)

        session = kwargs['session']

        if session.user_id != payload.uid:
            raise APIError(
                code=400,
                message="인증 세션과 탈퇴 세션의 유저 ID가 일치하지 않습니다."
            )

        return f(*args, **kwargs)

    return decorator
