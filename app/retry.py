from app.flag import set_flag as sf
from app.flag import check_flag as cf

prefix = "chick0/to-do:retry:{email}"


def set_flag(email: str) -> None:
    sf(prefix.format(email=email))


def check_flag(email: str) -> bool:
    return cf(prefix.format(email=email))
