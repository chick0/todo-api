from os import environ
from datetime import datetime
from datetime import timedelta

from jwt import encode
from jwt import decode
from jwt.exceptions import DecodeError
from flask import url_for

from app.mail import send_mail
from app.secret import get_secret
from app.error import VerifyFail

algorithms = ["HS256"]


def create_token(email: str) -> str:
    return encode(
        payload={
            "email": email,
            "exp": int((datetime.now() + timedelta(days=1)).timestamp())
        },
        key=get_secret("email_verify"),
        algorithm=algorithms[0]
    )


def send_verify_request(email: str) -> bool:
    token = create_token(email=email)

    send_mail(
        email=email,
        title="[To-Do] 이메일 인증 요청",
        html="\n".join([
            "<p>이 인증 요청은 1일뒤 만료됩니다.</p>",
            "<p>다음의 링크를 통해 인증할 수 있습니다.</p>",
            "<p>만약, 본인의 인증 시도가 아니라면 해당 링크로 들어가 '취소'를 선택하거나, 무시하면 됩니다.</p>",
            "<hr>",
            "<p>" + environ['HOST'] + url_for("email.verify", token=token) + "</p>"
        ])
    )

    return True


def decode_token(token: str) -> dict:
    try:
        return decode(
            jwt=token,
            key=get_secret("email_verify"),
            algorithms=algorithms
        )
    except DecodeError as de:
        raise VerifyFail(
            reason="인증 토큰 검증 실패"
        ) from de
