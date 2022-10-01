from app.routes.country import bp
from pydantic import BaseModel

from app.models import Country
from app.auth import AuthSession
from app.auth import login_required
from iso3166_1 import get_json


class CountryResponse(BaseModel):
    code: str
    name: str


class CodesResponse(BaseModel):
    status: bool = True
    message: str = ""
    codes: list[CountryResponse]


@bp.get("/codes")
@login_required
def codes(session: AuthSession):
    using_codes = [
        x.code
        for x in Country.query.filter_by(
            owner=session.user_id
        ).with_entities(
            Country.code
        ).all()
    ]

    return CodesResponse(
        codes=[
            CountryResponse(
                code=x[0],
                name=x[1]
            )
            for x in get_json().items()
            if x[0] not in using_codes
        ]
    ).dict()
