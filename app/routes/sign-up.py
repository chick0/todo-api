from hashlib import sha512
from datetime import datetime

from flask import Blueprint
from flask import request
from pydantic import BaseModel

from app import db
from app.models import User
from app.error import APIError
from app.response import BaseResponse
from app.verify import send_verify_request

bp = Blueprint("sign-up", __name__, url_prefix="/api/sign-up")


class SignUpRequest(BaseModel):
    email: str
    password: str


@bp.post("")
def sign_up():
    ctx = SignUpRequest(**request.json)

    if len(ctx.password) < 8:
        raise APIError(
            code=400,
            message="비밀번호를 8자리 이상으로 설정해야합니다."
        )

    ctx.password = sha512(ctx.password.encode("utf-8")).hexdigest()

    user = User.query.filter_by(
        email=ctx.email,
        password=ctx.password
    ).first()

    if user is not None:
        return BaseResponse(
            message="이미 가입한 이메일입니다! 비밀번호를 잊은 경우 '계정 찾기'를 통해 비밀번호를 재설정해야합니다."
        ).dict()

    del user

    user = User()
    user.email = ctx.email
    user.password = ctx.password
    user.created_at = datetime.now()
    user.lastlogin = None
    user.email_verified = False

    db.session.add(user)
    db.session.commit()

    result = send_verify_request(
        user_id=user.id,
        email=ctx.email
    )

    if result is True:
        return BaseResponse(
            message="가입이 완료되었습니다! 이메일 인증 이후 계정을 사용할 수 있습니다."
        ).dict(), 201
    else:
        db.session.delete(user)
        db.session.commit()

        raise APIError(
            code=500,
            message="이메일 인증 요청 전송에 실패해, 가입이 취소되었습니다."
        )
