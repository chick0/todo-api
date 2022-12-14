from flask import Blueprint
from pydantic import BaseModel

from app import db
from app.models import DBSession
from app.auth import AuthSession
from app.auth import login_required
from app.response import BaseResponse

bp = Blueprint("session", __name__, url_prefix="/api/session")


class DeleteRequest(BaseModel):
    id: int


@bp.delete("/all")
@login_required
def delete_all(session: AuthSession):
    DBSession.query.filter_by(
        owner=session.user_id
    ).delete()

    db.session.commit()

    return BaseResponse().dict()


@bp.delete("/<int:session_id>")
@login_required
def delete_one(session_id: int, session: AuthSession):
    DBSession.query.filter_by(
        id=session_id,
        owner=session.user_id
    ).delete()

    db.session.commit()

    return BaseResponse().dict()
