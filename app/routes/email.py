from datetime import datetime

from flask import Blueprint
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template

from app import db
from app.models import User
from app.verify import parse_token

bp = Blueprint("email", __name__, url_prefix="/api/email")


@bp.get("")
def verify():
    token: str = request.args.get("token", "").strip()

    if len(token) == 0:
        return "인증 토큰이 없습니다."

    payload = parse_token(token=token)

    return render_template(
        "verify.html",
        email=payload.email,
        date=datetime.fromtimestamp(payload.exp).strftime("%Y-%m-%d %H:%M:%S"),
        token=token,
    )


@bp.post("/drop")
def verify_drop():
    token = request.form.get("token", "")
    payload = parse_token(token=token)

    user: User = User.query.filter_by(
        email=payload.email
    ).first()

    if user is None:
        return redirect(url_for("email.verify_none"))

    if user.email_verified:
        return redirect(url_for("email.verify_fail"))

    db.session.delete(user)
    db.session.commit()

    return "인증 시도가 취소 되었으며 계정이 삭제됩니다."


@bp.post("/pass")
def verify_pass():
    token = request.form.get("token", "")
    payload = parse_token(token=token)

    user: User = User.query.filter_by(
        email=payload.email
    ).first()

    if user is None:
        return redirect(url_for("email.verify_none"))

    if user.email_verified:
        return redirect(url_for("email.verify_fail"))

    user.email_verified = True
    db.session.commit()

    return "인증 시도가 승인 되었으며 지금부터 계정을 사용 할 수 있습니다."


@bp.get("/fail")
def verify_fail():
    return "해당 인증 시도는 이미 통과되었습니다."


@bp.get("/none")
def verify_none():
    return "해당 계정은 탈퇴된 계정입니다."
