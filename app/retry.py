from app.utils import get_redis

prefix = "chick0/to-do:retry:"


def set_flag(email: str):
    redis = get_redis()
    return redis.set(
        name=prefix + email,
        value=b"true",
        ex=5 * 60
    )


def check_flag(email: str) -> bool:
    redis = get_redis()
    return redis.get(
        name=prefix + email
    ) == b"true"
