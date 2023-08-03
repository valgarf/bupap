import logging
import secrets
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import sqlalchemy as sa
from fastapi import HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from icecream import install
from loguru import logger
from nicegui import app, dependencies, ui
from starlette.middleware.sessions import SessionMiddleware

from bupap import db, permissions
from bupap.avatar import install_style, random_avatar
from bupap.config import settings
from bupap.db.testdata import add_testdata
from bupap.entrypoint.bupap_alembic import upgrade_head
from bupap.injection import Inject
from bupap.log_config import configure_logging
from bupap.ui import crud, page
from bupap.ui.common import LoginRequiredException
from bupap.ui.component import Gantt, Router

MAIN_FILE = Path(__file__).resolve()


def update_database():
    # TODO: we need to ensure that alembic is installed alongside the project and we need to find the .ini file
    # alembicArgs = [
    #     '--raiseerr',
    #     'upgrade', 'head',
    # ]
    # alembic.config.main(argv=alembicArgs)
    pass


def initialise_database():
    db.check_db_defaults(settings.initial_admin_password)
    if settings.testdata:
        add_testdata()


def initialise_injection():
    container = Inject()
    container.wire(packages=[crud])
    return container


def run():
    if settings.editable:
        install()
        ic.configureOutput(includeContext=True)
    upgrade_head()
    configure_logging()
    injection_container = initialise_injection()
    install_style()
    update_database()
    initialise_database()

    # with ui.column().classes("window-height window-width"):
    # with ui.column():
    #     counter = Gantt('Estimated Timeline', on_change=lambda msg: ui.notify(f'The value changed to {msg["args"]}.'))
    #     btn = ui.button("Update", on_click=lambda *args, **kwargs: counter.random())

    # TODO: only for testing! can use secrets.token_urlsafe(12) if none is given in config
    app.add_middleware(SessionMiddleware, secret_key="testing_mode")  # use your own secret key here

    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        with db.session() as session:
            request.state.session = session
            response = await call_next(request)
        return response

    @app.exception_handler(LoginRequiredException)
    async def login_required(request, exc):
        return RedirectResponse("/login")

    @app.exception_handler(Exception)
    async def general_exception(request, exc):
        try:
            ui.notify(f"{type(exc)!s}: {exc!s}")
        except Exception:
            # could not reach frontend (client not yet connected?)
            logger.opt(exception=exc).error("Failed to display exception to user:")
        raise HTTPException(status_code=500, detail="Internal server error")
    
    page.create_all_pages()
    ui.run(
        port=settings.port,
        title="bupap",
        host=settings.host,
        show=settings.show,
        binding_refresh_interval=10,
        reload=settings.editable, # only reload in editable mode
        uvicorn_reload_dirs = settings.pkg_root
    )


def run_poetry():
    # Note: somewhat of an evil hack. nicegui starts multiple processes and requires to run the
    # nicegui framework from these processes (i.e. __name__ == '__mp_main__' must run the app).
    # Poetry installs scripts with __name__ == '__mp_main__' only. So we run this function from
    # poetry, which then runs this file with the correct guards (see below).
    subprocess.run([sys.executable, str(MAIN_FILE)] + sys.argv[1:])


if __name__ in ["__main__", "__mp_main__"]:
    run()
