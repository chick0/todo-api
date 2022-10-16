from typing import Optional
from datetime import datetime

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
from app.utils import timestamp


class NoticeEditRequest(BaseModel):
    id: int
    title: Optional[str]
    text: Optional[str]


class NoticeEdit(BaseModel):
    title: Optional[str]
    text: Optional[str]
    updated_at: Optional[int]


class NoticeEditResponse(BaseResponse):
    notice: NoticeEdit


@bp.patch("")
@login_required
@admin_required
def edit(session: AuthSession):
    ctx = NoticeEditRequest(**request.json)

    notice: Notice = Notice.query.filter_by(
        id=ctx.id
    ).first()

    if notice is None:
        raise APIError(
            code=404,
            message="등록된 공지사항이 아닙니다."
        )

    if ctx.title is not None:
        notice.title = ctx.title.strip()[:80]

    if ctx.text is not None:
        notice.text = ctx.text.strip()

    notice.updated_at = datetime.now()

    db.session.commit()

    return NoticeEditResponse(
        message="공지가 수정되었습니다.",
        notice=NoticeEdit(
            title=notice.title,
            text=notice.text,
            updated_at=timestamp(notice.updated_at)
        )
    ).dict()
