from os import environ
from datetime import datetime

from flask import request
from flask import current_app as app
from redis import Redis
from user_agents import parse


def get_ip() -> str:
    return request.headers.get("X-Forwarded-For", request.remote_addr)


def timestamp(stamp: datetime) -> int or None:
    if stamp is None:
        return None

    return int(stamp.timestamp())


def parse_user_agent(user_agent: str) -> str:
    ua = parse(user_agent)
    return f"{ua.get_device()} / {ua.get_os()}"


def get_help_mail() -> str:
    help_email = environ['HELP_EMAIL'].strip()

    if help_email == ":SMTP_USER":
        help_email = environ['SMTP_USER']

    return help_email


def get_redis() -> Redis:
    return app.redis
