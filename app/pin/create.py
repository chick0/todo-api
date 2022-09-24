from re import findall
from typing import Optional
from hashlib import sha512
from datetime import datetime

from flask import request
from pydantic import BaseModel

from app.routes.pin import bp
from app import db
from app.models import Pin
from app.auth import AuthSession
from app.auth import login_required
from app.pin import create_token
from app.utils import get_ip


class PinCreateRequest(BaseModel):
    code: str


class PinCreateResponse(BaseModel):
    status: bool
    message: str
    token: Optional[str]


@bp.post("")
@login_required
def create(session: AuthSession):
    ctx = PinCreateRequest(**request.json)

    if len(ctx.code) < 6:
        return PinCreateResponse(
            status=False,
            message="6자리 이상으로 설정해야 합니다."
        ).dict(), 400

    if len(ctx.code) != len(findall(r"\d", ctx.code)):
        return PinCreateResponse(
            status=False,
            message="PIN은 숫자로 입력해야 합니다."
        ).dict(), 400

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
        status=True,
        message="PIN이 설정되었습니다. 설정된 PIN은 '계정 정보'에서 관리 할 수 있습니다.",
        token=token
    ).dict(), 201
