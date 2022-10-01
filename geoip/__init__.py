from os.path import join
from os.path import abspath
from os.path import dirname

from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError
from pydantic import BaseModel

from iso3166_1 import get_name

BASE_DIR = dirname(abspath(__file__))
DATA_PATH = join(BASE_DIR, "GeoLite2-Country.mmdb")


class IP(BaseModel):
    ip: str
    code: str
    name: str


def search(ip: str) -> IP:
    with Reader(DATA_PATH) as reader:
        try:
            response = reader.country(ip)
        except AddressNotFoundError:
            return IP(
                ip=ip,
                code="--",
                name="--"
            )

        code = response.country.iso_code

        return IP(
            ip=ip,
            code=code,
            name=get_name(response.country.iso_code)
        )
