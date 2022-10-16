from app.routes.notice import bp

from app.models import Notice
from app.notice import NoticeResponse
from app.response import BaseResponse
from app.utils import timestamp


class NoticeList(BaseResponse):
    notice_list: list[NoticeResponse]


@bp.get("")
def fetch():
    return NoticeList(
        notice_list=[
            NoticeResponse(
                id=x.id,
                title=x.title,
                text=x.text,
                created_at=timestamp(x.created_at),
                updated_at=None if x.updated_at is None else timestamp(x.updated_at)
            )
            for x in Notice.query.order_by(
                Notice.created_at.desc()
            ).all()
        ]
    ).dict()
