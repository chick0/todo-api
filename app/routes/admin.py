from flask import Blueprint
from pydantic import BaseModel

from app.models import Admin
from app.auth import AuthSession
from app.auth import login_required


bp = Blueprint("admin", __name__, url_prefix="/api/admin")


class AdminResponse(BaseModel):
    admin: bool


@bp.get("")
@login_required
def is_admin(session: AuthSession):
    admin: Admin = Admin.query.filter_by(
        user=session.user_id
    ).first()

    if admin is None:
        return AdminResponse(
            admin=False
        ).dict(), 400

    return AdminResponse(
        admin=True
    ).dict()
