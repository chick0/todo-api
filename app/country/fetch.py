from app.routes.country import bp
from pydantic import BaseModel

from app.models import Country
from app.auth import AuthSession
from app.auth import login_required
from app.utils import get_ip
from app.utils import timestamp
from geoip import search
from iso3166_1 import get_name


class CountryResponse(BaseModel):
    id: int
    name: str
    created_at: int


class FetchResponse(BaseModel):
    status: bool = True
    message: str = ""
    code: str
    name: str
    countrys: list[CountryResponse]


@bp.get("")
@login_required
def fetch(session: AuthSession):
    ip = search(ip=get_ip())

    return FetchResponse(
        code=ip.code,
        name=ip.name,
        countrys=[
            CountryResponse(
                id=x.id,
                name=get_name(x.code),
                created_at=timestamp(x.created_at)
            )
            for x in Country.query.filter_by(
                owner=session.user_id
            ).all()
        ]
    ).dict()
