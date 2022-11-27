from os import environ
from typing import Optional
from datetime import datetime

from flask import request
from flask import current_app as app
from redis import Redis
from user_agents import parse


def get_ip() -> str:
    remote_addr = request.remote_addr

    if remote_addr is None:
        remote_addr = "?"

    return request.headers.get("X-Forwarded-For", remote_addr)


def timestamp(stamp: datetime) -> Optional[int]:
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
    return app.config['redis']
