from datetime import datetime

from flask import Blueprint
from pydantic import BaseModel

from app import db
from app.models import Todo
from app.models import History
from app.models import DBSession
from app.auth import AuthSession
from app.auth import login_required
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
    dropped_at: int
    last_access: int


class UserResponse(BaseModel):
    status: bool
    count: int
    history_list: list[HistoryResponse]
    session_list: list[SessionResponse]


@bp.get("")
@login_required
def fetch(session: AuthSession):
    return UserResponse(
        status=True,
        count=Todo.query.filter_by(
            owner=session.user_id
        ).count(),
        history_list=[
            HistoryResponse(
                id=history.id,
                created_at=timestamp(history.created_at),
                ip=history.ip,
                device=parse_user_agent(history.user_agent)
            )
            for history in History.query.filter_by(
                owner=session.user_id
            ).order_by(
                History.created_at.asc()
            ).limit(80).all()
        ],
        session_list=[
            SessionResponse(
                id=dbs.id,
                history_id=dbs.history,
                dropped_at=timestamp(dbs.dropped_at),
                last_access=timestamp(dbs.last_access)
            )
            for dbs in DBSession.query.filter_by(
                owner=session.user_id
            ).filter(
                DBSession.dropped_at >= datetime.now()
            ).order_by(
                DBSession.dropped_at.asc()
            ).all()
        ]
    ).dict()


@bp.get("/count")
@login_required
def fetch_count_only(session: AuthSession):
    return UserResponse(
        status=True,
        count=Todo.query.filter_by(
            owner=session.user_id
        ).count(),
        history_list=[],
        session_list=[]
    ).dict()
