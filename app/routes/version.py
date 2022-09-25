from flask import Blueprint
from flask import current_app as app
from pydantic import BaseModel

from app.utils import timestamp

bp = Blueprint("version", __name__, url_prefix="/api/version")


class Version(BaseModel):
    id: str
    started_at: int


@bp.get("")
def get_version():
    return Version(
        id=app.commit_hash,
        started_at=timestamp(app.started_at)
    ).dict()
