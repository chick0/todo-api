from re import findall
from hashlib import sha512
from datetime import datetime

from flask import request
from app.routes.pin import bp
from pydantic import BaseModel

from app import db
from app.models import Pin
from app.auth import AuthSession
from app.auth import login_required
from app.pin import create_token
from app.error import APIError
from app.response import BaseResponse
from app.utils import get_ip


class PinCreateRequest(BaseModel):
    code: str


class PinCreateResponse(BaseResponse):
    token: str


@bp.post("")
@login_required
def create(session: AuthSession):
    ctx = PinCreateRequest(**request.json)

    if len(ctx.code) < 6:
        raise APIError(
            code=400,
            message="6자리 이상으로 설정해야 합니다."
        )

    if len(ctx.code) != len(findall(r"\d", ctx.code)):
        raise APIError(
            code=400,
            message="PIN은 숫자로 입력해야 합니다."
        )

    MAX_PIN = 5

    if Pin.query.filter_by(
        owner=session.user_id
    ).count() >= MAX_PIN:
        raise APIError(
            code=400,
            message=f"{MAX_PIN}개보다 많은 PIN을 등록 할 수 없습니다."
        )

    ctx.code = sha512(ctx.code.encode()).hexdigest()

    pin = Pin()
    pin.owner = session.user_id
    pin.created_at = datetime.now()
    pin.fail_count = 0
    pin.ip = get_ip()
    pin.user_agent = str(request.user_agent).strip()[:500]
    pin.last_access = None
    pin.code = ctx.code

    db.session.add(pin)
    db.session.commit()

    token = create_token(
        pid=pin.id,
        uid=pin.owner
    )

    pin.signature = token.split(".")[-1]
    db.session.commit()

    return PinCreateResponse(
        message="PIN이 설정되었습니다. 설정된 PIN은 '계정 정보'에서 관리 할 수 있습니다.",
        token=token
    ).dict(), 201
