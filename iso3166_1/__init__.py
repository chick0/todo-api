from os.path import join
from os.path import abspath
from os.path import dirname
from json import loads

BASE_DIR = dirname(abspath(__file__))
DATA_PATH = join(BASE_DIR, "data.json")


def get_json() -> dict:
    with open(DATA_PATH, mode="r", encoding="utf-8") as reader:
        json = loads(reader.read())
        return json


def get_name(code: str) -> str:
    try:
        return get_json()[code]
    except KeyError:
        return "-"
