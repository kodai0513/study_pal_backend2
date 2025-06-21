import os
from typing import Annotated, Generator

from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import Session, create_engine

dotenv_path = os.path.join(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ),
    ".env",
)
load_dotenv(dotenv_path)

_DB_HOST = os.getenv("DB_HOST")
_DB_NAME = os.getenv("DB_NAME")
_DB_PASSWORD = os.getenv("DB_PASSWORD")
_DB_PORT = os.getenv("DB_PORT")
_DB_USER = os.getenv("DB_USER")

_DATABASE_URL = f"mysql+mysqldb://{_DB_USER}:{_DB_PASSWORD}@{_DB_HOST}:{_DB_PORT}/{_DB_NAME}"

_engine = create_engine(
    _DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
)


def _get_session() -> Generator[Session, None, None]:
    session = Session(_engine)
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


SessionDep = Annotated[Session, Depends(_get_session)]
