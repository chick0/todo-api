from datetime import datetime

from app.routes.notice import bp
from flask import request
from pydantic import BaseModel

from app import db
from app.models import Notice
from app.auth import AuthSession
from app.auth import login_required
from app.admin import admin_required
from app.notice import NoticeResponse
from app.response import BaseResponse
from app.utils import timestamp


class NoticeRequest(BaseModel):
    title: str
    text: str


class NoticeCreateResponse(BaseResponse):
    notice: NoticeResponse


@bp.post("")
@login_required
@admin_required
def create(session: AuthSession):
    ctx = NoticeRequest(**request.json)

    notice = Notice()
    notice.owner = session.user_id
    notice.title = ctx.title.strip()[:80]
    notice.text = ctx.text.strip()
    notice.created_at = datetime.now()

    db.session.add(notice)
    db.session.commit()

    return NoticeCreateResponse(
        message="공지가 생성되었습니다.",
        notice=NoticeResponse(
            id=notice.id,
            title=notice.title,
            text=notice.text,
            created_at=timestamp(notice.created_at),
            updated_at=timestamp(notice.updated_at)
        )
    ).dict(), 201
