from os import environ
from datetime import datetime
from datetime import timedelta

from flask import url_for
from pydantic import BaseModel

from app.mail import send_mail
from app.flag import set_flag as sf
from app.flag import check_flag as cf
from app.token import create_token as ct
from app.token import parse_token as pt

prefix = "chick0/to-do:reset:{email}"
name = "verify:reset"


class ResetToken(BaseModel):
    user_id: int
    email: str
    exp: int


def set_flag(email: str) -> None:
    sf(prefix.format(email=email))


def check_flag(email: str) -> bool:
    return cf(prefix.format(email=email))


def create_token(user_id: int, email: str) -> str:
    payload = ResetToken(
        user_id=user_id,
        email=email,
        exp=int((datetime.now() + timedelta(hours=1)).timestamp())
    ).dict()

    return ct(payload, name)


def parse_token(token: str) -> ResetToken:
    return ResetToken(**pt(token, name))


def send_reset_request(user_id: int, email: str) -> bool:
    token = create_token(user_id=user_id, email=email)

    send_mail(
        email=email,
        title="[To-Do] 비밀번호 재설정 요청",
        html="\n".join([
            "<p>이 인증 요청은 1시간뒤 만료됩니다.</p>",
            "<p>다음의 링크를 통해 비밀번호를 재설정 할 수 있습니다.</p>",
            "<hr>",
            "<p>" + environ['HOST'] + url_for("reset.reset", token=token) + "</p>"
        ])
    )

    return True
