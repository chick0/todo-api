from flask import Blueprint

from app.utils import get_help_mail
from app.response import BaseResponse

bp = Blueprint("help", __name__, url_prefix="/api/help")


class HelpMailResponse(BaseResponse):
    email: str


@bp.get("")
def help_mail():
    return HelpMailResponse(
        email=get_help_mail()
    ).dict()
