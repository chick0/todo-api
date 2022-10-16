from app.routes.notice import bp
from flask import request
from pydantic import BaseModel

from app import db
from app.models import Notice
from app.auth import AuthSession
from app.auth import login_required
from app.admin import admin_required
from app.error import APIError
from app.response import BaseResponse


class NoticeDeleteRequest(BaseModel):
    id: int


@bp.delete("")
@login_required
@admin_required
def delete(session: AuthSession):
    ctx = NoticeDeleteRequest(**request.json)

    notice = Notice.query.filter_by(
        id=ctx.id
    ).delete()

    if notice == 0:
        raise APIError(
            code=404,
            message="등록된 공지가 아닙니다."
        )

    db.session.commit()

    return BaseResponse(
        message="공지가 삭제되었습니다."
    ).dict()
