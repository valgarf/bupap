from typing import overload

import sqlalchemy as sa

from bupap import db
from bupap.ui.viewmodel.team import NewTeam

from .common import return_obj_or_id


@overload
def create_team(project: NewTeam, external_session: None) -> int:
    ...


@overload
def create_team(project: NewTeam, external_session: db.Session) -> db.Team:
    ...


def create_team(team: NewTeam, external_session: db.Session | None = None):
    if not team.name:
        raise RuntimeError("Incomplete data to create a project.")
    with db.use_or_open_session(external_session) as session:
        db_team = db.Team(name=team.name)
        session.add(db_team)
        return return_obj_or_id(external_session, session, db_team)


def assign_team_role(
    team_id: int, user_id: int, role: int | str, external_session: db.Session | None = None
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
        db_team = session.get(db.Team, team_id)
        if db_team is None:
            raise RuntimeError(f"Team {team_id} could not be found in the database.")

        for assigned_role in db_user.team_roles:
            if assigned_role.team_id == team_id and assigned_role.role_id == db_role.id:
                raise RuntimeError(
                    f"User {db_user.name} already has role {db_role.name} for team {db_team.name}"
                )

        session.add(db.AssignedTeamRole(user=db_user, team=db_team, role=db_role))


def unassign_team_role(
    team_id: int, user_id: int, role: int | str, external_session: db.Session | None = None
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
        db_team = session.get(db.Team, team_id)
        if db_team is None:
            raise RuntimeError(f"Team {team_id} could not be found in the database.")

        for assigned_role in db_user.team_roles:
            if assigned_role.team_id == team_id and assigned_role.role_id == db_role.id:
                session.delete(assigned_role)
                break
        else:
            raise RuntimeError(
                f"User {db_user.name} does not have role {db_role.name} for team {db_team.name}"
            )


def assign_team_project(team_id: int, project_id: int, external_session: db.Session | None = None):
    with db.use_or_open_session(external_session) as session:
        db_team = session.get(db.Team, team_id)
        if db_team is None:
            raise RuntimeError(f"Team {team_id} could not be found in the database.")
        db_project = session.get(db.Project, project_id)
        if db_project is None:
            raise RuntimeError(f"Project {project_id} could not be found in the database.")

        if db_project in db_team.projects:
            raise RuntimeError(
                f"Project {db_project.name} and team {db_team.name} are already linked."
            )
        else:
            db_team.projects.append(db_project)


def unassign_team_project(
    team_id: int, project_id: int, external_session: db.Session | None = None
):
    with db.use_or_open_session(external_session) as session:
        db_team = session.get(db.Team, team_id)
        if db_team is None:
            raise RuntimeError(f"Team {team_id} could not be found in the database.")
        db_project = session.get(db.Project, project_id)
        if db_project is None:
            raise RuntimeError(f"Project {project_id} could not be found in the database.")

        if db_project in db_team.projects:
            db_team.projects.remove(db_project)
        else:
            raise RuntimeError(f"Project {db_project.name} and team {db_team.name} are not linked.")
