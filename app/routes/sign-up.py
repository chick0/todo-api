from hashlib import sha512
from datetime import datetime

from flask import Blueprint
from flask import request
from pydantic import BaseModel

from app import db
from app.models import User
from app.verify import send_verify_request

bp = Blueprint("sign-up", __name__, url_prefix="/api/sign-up")


class SignUpRequest(BaseModel):
    email: str
    password: str


class SignUpResponse(BaseModel):
    status: bool
    message: str


@bp.post("")
def sign_up():
    ctx = SignUpRequest(**request.json)

    password = sha512(ctx.password.encode("utf-8")).hexdigest()

    user = User.query.filter_by(
        email=ctx.email,
        password=password
    ).first()

    if user is not None:
        return SignUpResponse(
            status=False,
            message="이미 가입한 이메일입니다! 비밀번호를 잊은 경우 계정 찾기를 통해 비밀번호를 재설정하세요."
        ).dict()

    del user

    result = send_verify_request(
        email=ctx.email
    )

    if result is True:
        user = User()
        user.email = ctx.email
        user.password = password
        user.created_at = datetime.now()
        user.lastlogin = None
        user.email_verified = None

        db.session.add(user)
        db.session.commit()

        return SignUpResponse(
            status=True,
            message="가입이 완료되었습니다! 이메일 인증 이후 계정을 사용할 수 있습니다."
        ).dict()
    else:
        return SignUpResponse(
            status=False,
            message="이메일 인증 요청 전송에 실패해, 가입이 취소되었습니다."
        ).dict()
