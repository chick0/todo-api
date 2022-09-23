from app.utils import get_redis


def set_flag(name: str) -> None:
    redis = get_redis()
    redis.set(
        name=name,
        value=b"true",
        ex=5 * 60
    )


def check_flag(name: str) -> bool:
    redis = get_redis()
    return redis.get(
        name=name
    ) == b"true"
