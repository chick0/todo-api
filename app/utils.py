from flask import request
from user_agents import parse


def get_ip() -> str:
    return request.headers.get("X-Forwarded-For", request.remote_addr)


def timestamp(stamp) -> int or None:
    if stamp is None:
        return None

    return int(stamp.timestamp())


def parse_user_agent(user_agent: str) -> str:
    ua = parse(user_agent)
    return f"{ua.get_device()} / {ua.get_os()}"
