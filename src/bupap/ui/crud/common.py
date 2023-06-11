from typing import Type, TypeVar, overload

from bupap import db

T = TypeVar("T", bound=db.Base)


@overload
def return_obj_or_id(external_session: db.Session, session: db.Session, obj: T) -> T:
    ...


@overload
def return_obj_or_id(external_session: None, session: db.Session, obj: T) -> int:
    ...


def return_obj_or_id(external_session, session, obj):
    if external_session is None:
        session.flush()
        return obj.id
    else:
        return obj


def get_from_id(session: db.Session, cls: Type[T], entry_id: int) -> T:
    db_result = session.get(cls, entry_id)
    if db_result is None:
        raise RuntimeError(
            f"{cls.__name__} with id '{entry_id}' could not be found in the database."
        )
    return db_result
