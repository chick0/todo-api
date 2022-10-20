from os.path import join
from typing import NamedTuple


class Packed(NamedTuple):
    commit: str
    name: str


def get_packed() -> list[Packed]:
    try:
        with open(join(".git", "packed-refs"), mode="r") as packed_reader:
            return [
                Packed(*x.strip().split(" ")) for x in
                packed_reader.readlines()
                if not x.startswith("#")
            ]
    except FileNotFoundError:
        return []


def get_commit_id() -> str:
    ref_head = None
    target = "ref:"

    with open(join(".git", "HEAD"), mode="r") as head_reader:
        for data in head_reader.read().split("\n"):
            if data.startswith(target):
                result = data[len(target):].strip()
                ref_head = result

    try:
        with open(join(".git", result), mode="r") as commit_reader:
            return commit_reader.read().strip()
    except FileNotFoundError:
        for packed in get_packed():
            if packed.name == ref_head:
                return packed.commit

    return "null"
