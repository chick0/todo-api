from sys import argv
from glob import glob
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
from subprocess import run


def get_files() -> list:
    return [
        x for x in glob("./dist/**", recursive=True)
    ]


def tape():
    try:
        hash = argv[1]
        hash = hash[:7]
    except IndexError:
        hash = None

    if hash is None:
        try:
            hash = run("git rev-parse --short HEAD", capture_output=True).stdout.decode().strip()
        except:  # noqa: E722
            hash = "undefined"

    files = get_files()

    print("total files:", len(files))

    with ZipFile(
        file=f"dist-{hash}.zip",
        mode="w",
        compression=ZIP_DEFLATED,
        compresslevel=9
    ) as zip:
        for file in files:
            print(" +", file), zip.write(file)


if __name__ == "__main__":
    tape()
