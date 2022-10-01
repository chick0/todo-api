from app.routes.country import bp
from flask import request
from pydantic import BaseModel

from app import db
from app.models import Country
from app.auth import AuthSession
from app.auth import login_required
from app.error import APIError


class DeleteRequest(BaseModel):
    id: int


class DeleteResponse(BaseModel):
    status: bool = True
    message: str = ""


@bp.delete("")
@login_required
def delete(session: AuthSession):
    ctx = DeleteRequest(**request.json)

    country = Country.query.filter_by(
        id=ctx.id,
        owner=session.user_id
    ).first()

    if country is None:
        raise APIError(
            code=404,
            message="등록된 허용 국가가 아닙니다."
        )

    db.session.delete(country)
    db.session.commit()

    return DeleteResponse().dict()
