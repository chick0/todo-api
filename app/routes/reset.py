from hashlib import sha512

from flask import Blueprint
from flask import request
from flask import render_template
from pydantic import BaseModel

from app import db
from app.models import User
from app.reset import send_reset_request
from app.reset import check_flag
from app.reset import set_flag
from app.reset import ResetToken
from app.reset import parse_token
from app.utils import get_help_mail

bp = Blueprint("reset", __name__, url_prefix="/api/reset")


class CreateResetRequest(BaseModel):
    email: str


class ResetRequest(BaseModel):
    password: str


class ResetResponse(BaseModel):
    status: bool
    message: str = ""


@bp.get("")
def reset():
    token: str = request.args.get("token", "").strip()

    if len(token) == 0:
        return "인증 토큰이 없습니다."

    return render_template(
        "reset.html",
        token=token
    )


@bp.post("/step1")
def create_reset_request():
    ctx = CreateResetRequest(**request.json)
    user: User = User.query.filter_by(
        email=ctx.email
    ).first()

    if user is None:
        return ResetResponse(
            status=False,
            message="등록된 계정이 아닙니다."
        ).dict(), 404

    if user.email_verified is False:
        return ResetResponse(
            status=False,
            message="이메일 인증이 완료되지 않은 계정은 사용 할 수 없습니다."
        ).dict(), 400

    if check_flag(email=ctx.email):
        return ResetResponse(
            status=False,
            message="5분마다 한 번씩 시도할 수 있습니다."
        ).dict(), 400

    result = send_reset_request(
        user_id=user.id,
        email=ctx.email
    )

    if result is True:
        set_flag(email=ctx.email)
        return ResetResponse(
            status=True,
            message="해당 이메일 주소로 비밀번호 재설정 링크를 전송했습니다."
        ).dict(), 201
    else:
        return ResetResponse(
            status=False,
            message="비밀번호 재설정 요청 전송에 실패했습니다. "
                    f"반복해서 실패하거나 해당 이메일 주소를 사용 할 수 없다면, {get_help_mail()}로 메일을 보내주세요."
        ).dict(), 500


@bp.post("/step2")
def reset_request():
    token: str = request.headers.get("x-reset", "").strip()
    payload: ResetToken = parse_token(token=token)

    user: User = User.query.filter_by(
        id=payload.user_id,
        email=payload.email,
        email_verified=True
    ).first()

    if user is None:
        return ResetResponse(
            status=False,
            message="등록된 계정이 아닙니다."
        ).dict(), 404

    ctx = ResetRequest(**request.json)
    ctx.password = sha512(ctx.password.encode()).hexdigest()

    user.password = ctx.password
    db.session.commit()

    return ResetResponse(
        status=True,
        message="비밀번호가 재설정되었습니다."
    ).dict()
