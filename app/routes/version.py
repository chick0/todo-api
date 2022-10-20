from flask import Blueprint
from flask import current_app as app
from pydantic import BaseModel

bp = Blueprint("version", __name__, url_prefix="/api/version")


class Version(BaseModel):
    started_at: int
    commit: str


@bp.get("")
def get_version():
    return Version(**app.config['VERSION']).dict()
