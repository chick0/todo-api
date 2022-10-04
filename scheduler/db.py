from os import environ

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if "SQLALCHEMY_DATABASE_URI" not in environ:
    load_dotenv()

SQLALCHEMY_DATABASE_URI = environ['SQLALCHEMY_DATABASE_URI']

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URI,
    pool_size=5,
    max_overflow=10
)

factory = sessionmaker(bind=engine)
