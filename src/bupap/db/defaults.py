import secrets

import sqlalchemy as sa
from loguru import logger

from bupap import permissions
from bupap.avatar import random_avatar

from . import session as db_session
from .tables import AssignedGlobalRole, EstimateType, Role, RoleType, Timesink, User


def check_admin_exists(initial_password: str | None = None):
    password = initial_password
    if password is None:
        password = secrets.token_urlsafe(12)
    with db_session() as session:
        admin_user = session.scalars(sa.select(User).where(User.name == "admin")).first()
        admin_role = session.scalars(sa.select(Role).where(Role.name == "Admin")).first()
        assert admin_role is not None
        if not admin_user:
            user = User(name="admin", full_name="Administrator", avatar=random_avatar())
            user.set_password(password)
            session.add(user)
            session.add(AssignedGlobalRole(user=user, role=admin_role))
            if initial_password is None:
                logger.warning(
                    "Adding user 'admin' with random initial password '{}'. Please change immediatly! Note: Using the 'initial_admin_password' configuration allows to set a fixed initial password if no admin account exists)",
                    password,
                )
            else:
                logger.warning(
                    "Adding user 'admin' with configured initial password (see config). Please change immediatly!"
                )


def check_builtin_roles_exist():
    with db_session() as session:
        roles = {r.name: r for r in session.scalars(sa.select(Role).where(Role.builtin == True))}
        for role_type, default_roles in [
            (RoleType.GLOBAL, permissions.default_global_roles),
            (RoleType.PROJECT, permissions.default_project_roles),
            (RoleType.TEAM, permissions.default_team_roles),
        ]:
            for name, perm in default_roles.items():
                if name not in roles:
                    session.add(
                        Role(name=name, permissions=perm, builtin=True, role_type=role_type)
                    )


def check_builtin_timesinks_exist():
    with db_session() as session:
        for name in ["Meeting", "Customer Support", "Assisstance", "Planning", "Review", "Other"]:
            db_timesink = session.scalars(sa.select(Timesink).where(Timesink.name == name)).first()
            if db_timesink is None:
                session.add(Timesink(name=name, color="#fff176"))


def check_builtin_estimate_types_exist():
    with db_session() as session:
        builtin_types = {
            "Precise": {
                "description": "For very precise estimates. Suggestion: +/- 1 hour",
                "relative": False,
                "optimistic": -3600,
                "average": 0,
                "pessimistic": +3600,
                "min": 10,
                "max": 100,
            },
            "Thought-out": {
                "description": "For planned tasks after careful consideration. Suggestion: -25% / +100%.",
                "relative": True,
                "optimistic": 0.75,
                "average": 1.25,
                "pessimistic": 2,
                "min": 10,
                "max": 100,
            },
            "Gut Feeling": {
                "description": "For vague estimates. Suggestion: -50% / +200%",
                "relative": True,
                "optimistic": 0.5,
                "average": 1.5,
                "pessimistic": 3,
                "min": 10,
                "max": 100,
            },
        }
        for name, data in builtin_types.items():
            db_estimate_type = session.scalars(
                sa.select(EstimateType).where(EstimateType.name == name)
            ).first()
            if db_estimate_type is None:
                session.add(
                    EstimateType(
                        name=name,
                        description=data["description"],
                        relative=data["relative"],
                        default_shift_optimistic=data["optimistic"],
                        default_shift_pessimistic=data["pessimistic"],
                        default_shift_average=data["average"],
                        min_datapoints=data["min"],
                        max_datapoints=data["max"],
                    )
                )


def check_db_defaults(initial_admin_password: str | None):
    check_builtin_roles_exist()
    check_admin_exists(initial_admin_password)
    check_builtin_timesinks_exist()
    check_builtin_estimate_types_exist()
