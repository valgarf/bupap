from typing import overload

import sqlalchemy as sa

from bupap import db
from bupap.ui.viewmodel.user import NewUser

from .common import return_obj_or_id


@overload
def create_user(project: NewUser, external_session: db.Session) -> db.User:
    ...


@overload
def create_user(project: NewUser, external_session: None) -> int:
    ...



def create_user(user: NewUser, external_session: db.Session | None = None):
    if not user.name or not user.full_name or not user.password or not user.avatar:
        raise RuntimeError("Incomplete data to create a user.")
    with db.use_or_open_session(external_session) as session:
        db_user_role = session.scalars(sa.select(db.Role).where(db.Role.name == "User")).first()
        assert db_user_role is not None
        db_user = db.User(name=user.name, full_name=user.full_name, avatar=user.avatar)
        db_user.set_password(user.password)
        session.add(db_user)
        session.add(db.AssignedGlobalRole(user=db_user, role=db_user_role))
        return return_obj_or_id(external_session, session, db_user)
