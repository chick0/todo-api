from flask import Blueprint
from flask import request
from pydantic import BaseModel

from app.retry import set_flag
from app.retry import check_flag
from app.models import User
from app.verify import send_verify_request
from app.error import APIError
from app.response import BaseResponse

bp = Blueprint("retry", __name__, url_prefix="/api/retry")


class RetryRequest(BaseModel):
    email: str


@bp.post("")
def retry():
    ctx = RetryRequest(**request.json)
    user: User = User.query.filter_by(
        email=ctx.email
    ).first()

    if user is None:
        raise APIError(
            code=404,
            message="등록된 계정이 아닙니다."
        )

    if user.email_verified is True:
        return BaseResponse(
            message="이미 인증된 계정입니다."
        ).dict()

    if check_flag(email=ctx.email):
        raise APIError(
            code=400,
            message="5분마다 한 번씩 시도할 수 있습니다."
        )

    result = send_verify_request(
        user_id=user.id,
        email=user.email
    )

    if result is True:
        set_flag(email=ctx.email)
        return BaseResponse(
            message="이메일 인증 요청이 전송되었습니다! 이메일을 확인해주세요."
        ).dict(), 201
    else:
        raise APIError(
            code=500,
            message="이메일 인증 요청 전송에 실패했습니다."
        )
