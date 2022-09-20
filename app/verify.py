from os import environ
from datetime import datetime
from datetime import timedelta

from flask import url_for
from pydantic import BaseModel

from app.mail import send_mail
from app.token import create_token as ct
from app.token import parse_token as pt

name = "verify:email"


class EmailVerifyToken(BaseModel):
    user_id: int
    email: str
    exp: int


def create_token(user_id: int, email: str) -> str:
    payload = EmailVerifyToken(
        user_id=user_id,
        email=email,
        exp=int((datetime.now() + timedelta(days=1)).timestamp())
    ).dict()

    return ct(payload, name)


def parse_token(token: str) -> EmailVerifyToken:
    return EmailVerifyToken(**pt(token, name))


def send_verify_request(user_id: int, email: str) -> bool:
    token = create_token(user_id=user_id, email=email)

    send_mail(
        email=email,
        title="[To-Do] 이메일 인증 요청",
        html="\n".join([
            "<p>이 인증 요청은 1일뒤 만료됩니다.</p>",
            "<p>다음의 링크를 통해 인증할 수 있습니다.</p>",
            "<p>만약, 본인의 인증 시도가 아니라면 해당 링크로 들어가 '취소'를 선택하거나, 무시하면 됩니다.</p>",
            "<hr>",
            "<p>" + environ['HOST'] + url_for("verify.verify", token=token) + "</p>"
        ])
    )

    return True
