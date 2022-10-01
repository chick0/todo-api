from datetime import datetime

from app.routes.country import bp
from flask import request
from pydantic import BaseModel

from app import db
from app.models import Country
from app.auth import AuthSession
from app.auth import login_required
from app.error import APIError
from iso3166_1 import get_name


class CreateRequest(BaseModel):
    code: str


class CreateResponse(BaseModel):
    status: bool = True
    message: str = ""


@bp.post("")
@login_required
def create(session: AuthSession):
    ctx = CreateRequest(**request.json)
    name = get_name(code=ctx.code)

    if name == "-":
        raise APIError(
            code=400,
            message="등록된 국가가 아닙니다."
        )

    MAX_COUNTRY = 5

    if Country.query.filter_by(
        owner=session.user_id
    ).count() >= MAX_COUNTRY:
        raise APIError(
            code=400,
            message=f"최대 {MAX_COUNTRY}개까지 등록 할 수 있습니다."
        )

    if Country.query.filter_by(
        owner=session.user_id,
        code=ctx.code
    ).count() != 0:
        raise APIError(
            code=400,
            message="이미 허용한 국가 입니다."
        )

    country = Country()
    country.owner = session.user_id
    country.created_at = datetime.now()
    country.code = ctx.code

    db.session.add(country)
    db.session.commit()

    return CreateResponse().dict(), 201
