import cProfile
import logging
import os
import pstats
import random
import secrets
import string
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import sqlalchemy as sa
import uvicorn
from fastapi import HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from icecream import install
from loguru import logger
from nicegui import app, dependencies, ui
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from bupap import db, permissions
from bupap.avatar import install_style, random_avatar
from bupap.config import settings
from bupap.db.database import get_database
from bupap.db.testdata import add_testdata
from bupap.entrypoint.bupap_alembic import upgrade_head
from bupap.gql import ContextGraphql
from bupap.gql.schema import schema
from bupap.injection import Inject
from bupap.log_config import configure_logging
from bupap.ui import crud, page
from bupap.ui.common import LoginRequiredException
from bupap.ui.component import Gantt, Router

MAIN_FILE = Path(__file__).resolve()


def initialise_database():
    db.check_db_defaults(settings.initial_admin_password)
    if settings.testdata:
        add_testdata()


def startup():
    if settings.editable:
        install()
        ic.configureOutput(includeContext=True)
    upgrade_head()
    configure_logging()
    install_style()
    initialise_database()


class DBMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        with get_database().session() as session:
            from icecream import ic

            scope["db_session"] = session
            await self.app(scope, receive, send)


graphql_app = ContextGraphql(schema, debug=settings.editable)
secret_key = settings.session_secret
if not secret_key:
    secret_key = "".join(random.choices(string.ascii_letters + string.digits, k=16))
app = Starlette(
    debug=settings.editable,
    on_startup=[startup],
    middleware=[
        Middleware(
            CORSMiddleware, allow_origins=["*"], allow_headers=["*"], allow_credentials=True
        ),
        Middleware(DBMiddleware),
        Middleware(SessionMiddleware, secret_key=secret_key, https_only=False, same_site="lax"),
    ],
)
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)


def main():
    uvicorn.run(
        "bupap.entrypoint.strawberry_gql:app",
        port=settings.graphql_port,
        host=settings.host,
        log_level="info",
    )


if __name__ in ["__main__", "__mp_main__"]:
    main()
