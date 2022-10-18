from os.path import join
from os.path import abspath
from os.path import dirname
from os.path import isfile
from os import remove

BASE_DIR = dirname(dirname(abspath(__file__)))

DATABASE_DIR = f"sqlite:///{BASE_DIR}/test.db"

_db_path = join(BASE_DIR, "test.db")

if isfile(_db_path):
    remove(_db_path)

del _db_path
