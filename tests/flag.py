from os import environ


def set_flag(key: str, value: str):
    environ[f"flag_{key}"] = value


def get_flag(key: str) -> str or None:
    try:
        return environ[f"flag_{key}"]
    except KeyError:
        raise AssertionError(f"Undefined flag : {key}")
