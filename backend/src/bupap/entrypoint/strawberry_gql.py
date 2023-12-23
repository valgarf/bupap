import random
import string
from pathlib import Path

import uvicorn
from icecream import install
from loguru import logger
from nicegui import app
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from bupap import db
from bupap.avatar import install_style
from bupap.config import settings
from bupap.db.database import get_database
from bupap.db.testdata import add_testdata
from bupap.entrypoint.bupap_alembic import upgrade_head
from bupap.gql import ContextGraphql
from bupap.gql.schema import schema
from bupap.log_config import configure_logging

MAIN_FILE = Path(__file__).resolve()


def initialise_database():
    db.check_db_defaults(settings.initial_admin_password)
    if settings.testdata:
        add_testdata()


def startup():
    if settings.editable:
        install()
        ic.configureOutput(includeContext=True)
    configure_logging()
    upgrade_head()
    install_style()
    initialise_database()


class DBMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        with get_database().session() as session:
            scope["db_session"] = session
            await self.app(scope, receive, send)


graphql_app = ContextGraphql(schema, debug=settings.editable)
secret_key = settings.session_secret
if not secret_key:
    logger.warning(
        "No secret key for session defined. Using a random one. Restarts will log out users."
    )
    secret_key = "".join(random.choices(string.ascii_letters + string.digits, k=16))

app = Starlette(
    debug=settings.editable,
    on_startup=[startup],
    middleware=[
        Middleware(
            CORSMiddleware, allow_origins=["*"], allow_headers=["*"], allow_credentials=True
        ),
        Middleware(DBMiddleware),
        Middleware(
            SessionMiddleware,
            session_cookie="login_session",
            secret_key=secret_key,
            https_only=False,
            same_site="lax",
        ),
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
        reload=settings.uvicorn.reload,
    )


if __name__ in ["__main__", "__mp_main__"]:
    main()
