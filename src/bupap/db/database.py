from contextlib import contextmanager
from functools import cache
from pathlib import Path
from typing import Iterator

import sqlalchemy as sa
import sqlalchemy.orm

from bupap.config import settings


class _Database:
    def __init__(self):
        data_dir = settings.db.data_dir
        if data_dir:
            Path(data_dir).mkdir(parents=True, exist_ok=True)
        self.url = settings.db.url
        self.engine = sa.create_engine(self.url)
        self._sessionmaker = sa.orm.sessionmaker(self.engine)

    @contextmanager
    def session(self) -> Iterator[sa.orm.Session]:
        with self._sessionmaker() as session:
            try:
                yield session
                session.commit()
            except:
                session.rollback()
                raise


@cache
def get_database():
    return _Database()


@contextmanager
def session() -> Iterator[sa.orm.Session]:
    with get_database().session() as session:
        yield session


@contextmanager
def use_or_open_session(session: sa.orm.Session | None) -> Iterator[sa.orm.Session]:
    """
    Contextmanager to open a session if necessary. If given an existing session, it will simply
    yield it.

    Usage:
    ```
    def do_something(external_session: Session | None = None):
        with use_or_open_session(external_session) as session:
            # session is the same as `external_session` if one is provided, or a newly created one.
            ...
    """
    if session is not None:
        yield session
    else:
        with get_database().session() as new_session:
            yield new_session
