from flask import request
from app.routes.pin import bp
from pydantic import BaseModel

from app import db
from app.models import Pin
from app.auth import AuthSession
from app.auth import login_required
from app.error import APIError
from app.response import BaseResponse


class DeleteRequest(BaseModel):
    id: int


@bp.delete("")
@login_required
def delete(session: AuthSession):
    ctx = DeleteRequest(**request.json)

    pin: Pin = Pin.query.filter_by(
        id=ctx.id,
        owner=session.user_id
    ).first()

    if pin is None:
        raise APIError(
            code=404,
            message="등록된 PIN이 아닙니다."
        )

    db.session.delete(pin)
    db.session.commit()

    return BaseResponse(
        message="해당 PIN이 삭제되었습니다."
    ).dict(), 200
