from typing import overload

import sqlalchemy as sa

from bupap import db
from bupap.ui.viewmodel.project import NewProject

from .common import get_from_id, return_obj_or_id


@overload
def create_project(project: NewProject, external_session: db.Session) -> db.Project:
    ...


@overload
def create_project(project: NewProject, external_session: None) -> int:
    ...


def create_project(project, external_session=None):
    if not project.name:
        raise RuntimeError("Incomplete data to create a project.")
    with db.use_or_open_session(external_session) as session:
        db_parent = None
        if project.parent_id is not None:
            db_parent = get_from_id(session, db.Project, project.parent_id)
        db_project = db.Project(
            name=project.name,
            description=project.description,
            color=project.color,
            parent=db_parent,
        )
        session.add(db_project)
        return return_obj_or_id(external_session, session, db_project)


def assign_project_role(
    project_id: int, user_id: int, role: int | str, external_session: db.Session | None = None
):
    with db.use_or_open_session(external_session) as session:
        db_role = None
        if isinstance(role, str):
            db_role = session.scalars(sa.select(db.Role).where(db.Role.name == role)).one()
        else:
            db_role = session.get(db.Role, role)
        if db_role is None:
            raise RuntimeError(f"Role {role} could not be found in the database.")
        db_user = session.get(db.User, user_id)
        if db_user is None:
            raise RuntimeError(f"User {user_id} could not be found in the database.")
        db_project = session.get(db.Project, project_id)
        if db_project is None:
            raise RuntimeError(f"Project {project_id} could not be found in the database.")

        for assigned_role in db_user.project_roles:
            if assigned_role.project_id == project_id and assigned_role.role_id == db_role.id:
                raise RuntimeError(
                    f"User {db_user.name} already has role {db_role.name} for project {db_project.name}"
                )

        session.add(db.AssignedProjectRole(user=db_user, project=db_project, role=db_role))


def unassign_project_role(
    project_id: int, user_id: int, role: int | str, external_session: db.Session | None = None
):
    with db.use_or_open_session(external_session) as session:
        db_role = None
        if isinstance(role, str):
            db_role = session.scalars(sa.select(db.Role).where(db.Role.name == role)).one()
        else:
            db_role = session.get(db.Role, role)
        if db_role is None:
            raise RuntimeError(f"Role {role} could not be found in the database.")
        db_user = session.get(db.User, user_id)
        if db_user is None:
            raise RuntimeError(f"User {user_id} could not be found in the database.")
        db_project = session.get(db.Project, project_id)
        if db_project is None:
            raise RuntimeError(f"Project {project_id} could not be found in the database.")

        for assigned_role in db_user.project_roles:
            if assigned_role.project_id == project_id and assigned_role.role_id == db_role.id:
                session.delete(assigned_role)
                break
        else:
            raise RuntimeError(
                f"User {db_user.name} does not have role {db_role.name} for project {db_project.name}"
            )
