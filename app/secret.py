from json import dump
from json import load
from secrets import token_bytes

filename = ".jwt.json"


def _secret() -> dict:
    try:
        return load(fp=open(filename, mode="r", encoding="utf-8"))
    except FileNotFoundError:
        return {}


def get_secret(name: str) -> str:
    secret = _secret()

    try:
        return secret[name]
    except KeyError:
        return set_secret(name=name)


def set_secret(name: str) -> str:
    secret = _secret()

    new: str = token_bytes(48).hex()
    secret[name] = new 

    dump(secret, fp=open(filename, mode="w", encoding="utf-8"))
    return new
