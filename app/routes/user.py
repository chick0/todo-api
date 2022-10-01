from typing import Optional
from datetime import datetime

from flask import Blueprint
from flask import request
from pydantic import BaseModel

from app.models import Todo
from app.models import History
from app.models import DBSession
from app.models import Pin
from app.auth import token_ttl
from app.auth import AuthSession
from app.auth import login_required
from app.error import APIError
from app.utils import timestamp
from app.utils import parse_user_agent

bp = Blueprint("user", __name__, url_prefix="/api/user")


class HistoryResponse(BaseModel):
    id: int
    created_at: int
    ip: str
    device: str


class SessionResponse(BaseModel):
    id: int
    history_id: int
    created_at: int
    dropped_at: int
    last_access: Optional[int]
    device: str


class PinResponse(BaseModel):
    id: int
    created_at: int
    fail_count: int
    device: str
    last_access: Optional[int]


class UserResponse(BaseModel):
    status: bool = True
    message: str = ""
    count: int
    pin_list: list[PinResponse]
    session_list: list[SessionResponse]
    history_list: list[HistoryResponse]


class HistoryMoreResponse(BaseModel):
    status: bool = True
    message: str = ""
    history_list: list[HistoryResponse]


@bp.get("")
@login_required
def fetch(session: AuthSession):
    def calc_created_at(dbs: DBSession) -> datetime:
        return dbs.dropped_at - token_ttl

    def get_device(history_id: int) -> str:
        local = [x for x in history_list if x.id == history_id]

        if len(local) == 1:
            return parse_user_agent(local[0].user_agent)

        return parse_user_agent(
            History.query.filter_by(
                id=history_id,
                owner=session.user_id
            ).first().user_agent
        )

    history_list = History.query.filter_by(
        owner=session.user_id
    ).order_by(
        History.created_at.desc()
    ).limit(15).all()

    return UserResponse(
        count=Todo.query.filter_by(
            owner=session.user_id
        ).count(),
        pin_list=[
            PinResponse(
                id=pin.id,
                created_at=timestamp(pin.created_at),
                fail_count=pin.fail_count,
                device=parse_user_agent(pin.user_agent),
                last_access=timestamp(pin.last_access)
            )
            for pin in Pin.query.filter_by(
                owner=session.user_id
            ).order_by(
                Pin.last_access.desc()
            ).all()
        ],
        session_list=[
            SessionResponse(
                id=dbs.id,
                history_id=dbs.history,
                created_at=timestamp(calc_created_at(dbs)),
                dropped_at=timestamp(dbs.dropped_at),
                last_access=timestamp(dbs.last_access),
                device=get_device(history_id=dbs.history)
            )
            for dbs in DBSession.query.filter_by(
                owner=session.user_id
            ).filter(
                DBSession.dropped_at >= datetime.now()
            ).order_by(
                DBSession.last_access.desc()
            ).all()
        ],
        history_list=[
            HistoryResponse(
                id=history.id,
                created_at=timestamp(history.created_at),
                ip=history.ip,
                device=parse_user_agent(history.user_agent)
            )
            for history in history_list
        ]
    ).dict()


@bp.get("/more")
@login_required
def more(session: AuthSession):
    try:
        cursor = int(request.args.get("cursor", "-"))
    except (ValueError, TypeError):
        raise APIError(
            code=400,
            message="커서가 올바르지 않습니다."
        )

    history_list = History.query.filter_by(
        owner=session.user_id
    ).filter(
        History.id < cursor
    ).order_by(
        History.created_at.desc()
    ).limit(15).all()

    return HistoryMoreResponse(
        history_list=[
            HistoryResponse(
                id=history.id,
                created_at=timestamp(history.created_at),
                ip=history.ip,
                device=parse_user_agent(history.user_agent)
            )
            for history in history_list
        ]
    ).dict()
