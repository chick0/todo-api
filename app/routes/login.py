from hashlib import sha512
from datetime import datetime

from flask import Blueprint
from flask import request
from pydantic import BaseModel

from app import db
from app.models import User
from app.auth import create_token

bp = Blueprint("login", __name__, url_prefix="/api/login")


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    status: bool
    message: str = ""
    token: str = ""


@bp.post("")
def email_and_password():
    ctx = LoginRequest(**request.json)
    ctx.password = sha512(ctx.password.encode("utf-8")).hexdigest()

    user: User = User.query.filter_by(
        email=ctx.email,
        password=ctx.password
    ).first()

    if user is None:
        return LoginResponse(
            status=False,
            message="등록된 계정이 아닙니다."
        ).dict(), 404
    else:
        user.lastlogin = datetime.now()
        db.session.commit()

        return LoginResponse(
            status=True,
            token=create_token(
                email=user.email
            )
        ).dict()