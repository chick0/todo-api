from flask import Blueprint
from flask import request
from flask import render_template
from pydantic import BaseModel

from app import db
from app.models import User
from app.error import APIError
from app.response import BaseResponse
from app.verify import parse_token

bp = Blueprint("verify", __name__, url_prefix="/api/verify")


class VerifySessionResponse(BaseResponse):
    email: str
    exp: int


class VerifyAnswerRequest(BaseModel):
    # true : pass
    # false: drop
    answer: bool


@bp.get("")
def verify():
    token: str = request.args.get("token", "").strip()

    if len(token) == 0:
        return "인증 토큰이 없습니다."

    return render_template(
        "verify.html",
        token=token,
    )


@bp.get("/session")
def fetch_verify_session():
    token: str = request.headers.get("x-auth", "").strip()
    payload = parse_token(token=token)

    return VerifySessionResponse(
        email=payload.email,
        exp=payload.exp
    ).dict()


@bp.post("")
def verify_answer():
    token: str = request.headers.get("x-auth", "").strip()
    payload = parse_token(token=token)

    ctx = VerifyAnswerRequest(**request.json)

    user: User = User.query.filter_by(
        id=payload.user_id,
        email=payload.email
    ).first()

    if user is None:
        raise APIError(
            code=404,
            message="이미 삭제된 계정입니다."
        )

    if user.email_verified:
        raise APIError(
            code=400,
            message="이미 인증된 계정입니다."
        )

    if ctx.answer is True:
        user.email_verified = True
        db.session.commit()

        return BaseResponse(
            message="인증 시도가 승인 되었으며 지금부터 계정을 사용 할 수 있습니다."
        ).dict(), 201
    else:
        db.session.delete(user)
        db.session.commit()

        return BaseResponse(
            message="인증 시도가 취소 되었으며 계정이 삭제됩니다."
        ).dict()
