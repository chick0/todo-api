from flask import Blueprint
from pydantic import BaseModel

from app import db
from app.models import DBSession
from app.auth import AuthSession
from app.auth import login_required

bp = Blueprint("logout", __name__, url_prefix="/api/logout")


class LogoutResponse(BaseModel):
    status: bool = True


@bp.delete("")
@login_required
def logout(session: AuthSession):
    dbs = DBSession.query.filter_by(
        id=session.sid,
        owner=session.user_id
    ).delete()

    if dbs != 0:
        db.session.commit()

    return LogoutResponse().dict()
