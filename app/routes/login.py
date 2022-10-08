from hashlib import sha512

from flask import Blueprint
from flask import request
from pydantic import BaseModel

from app.models import User
from app.auth import create_auth_token
from app.error import APIError
from app.response import BaseResponse

bp = Blueprint("login", __name__, url_prefix="/api/login")


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseResponse):
    token: str = ""
    email_verify_required: bool = False


@bp.post("")
def email_and_password():
    ctx = LoginRequest(**request.json)
    ctx.password = sha512(ctx.password.encode("utf-8")).hexdigest()

    user: User = User.query.filter_by(
        email=ctx.email,
        password=ctx.password
    ).first()

    if user is None:
        raise APIError(
            code=404,
            message="등록된 계정이 아닙니다."
        )

    if not user.email_verified:
        return LoginResponse(
            status=False,
            message="이메일 인증이 완료되지 않은 계정은 사용 할 수 없습니다.",
            email_verify_required=True
        ).dict(), 400

    return LoginResponse(
        token=create_auth_token(user=user)
    ).dict(), 201
