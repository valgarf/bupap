from __future__ import annotations

import uuid
from functools import partial

import sqlalchemy as sa
from fastapi import Request
from fastapi.responses import RedirectResponse
from loguru import logger
from nicegui import ui
from starlette.middleware.sessions import SessionMiddleware

from bupap import db
from bupap.ui import viewmodel
from bupap.ui.common import get_user


def create_login_page():
    @ui.page("/login")
    def login_page(request: Request):
        user = get_user(request, required=False)
        if user is not None:
            return RedirectResponse("/")
        request.session["id"] = str(uuid.uuid4())
        login_info = viewmodel.LoginInformation(session_id=request.session["id"])
        login_func = partial(try_login, login_info)
        with ui.row().classes("absolute-center"):
            with ui.card():
                ui.input("Username").bind_value(login_info, "username").classes("full-width")
                ui.input("Password", password=True, password_toggle_button=True).bind_value(
                    login_info, "password"
                ).on("keydown.enter", login_func)
                with ui.row().classes("justify-center full-width"):
                    ui.button("Login", on_click=login_func)


def try_login(login_info: viewmodel.LoginInformation, event):
    success = False
    with db.session() as session:
        user: db.User = session.scalars(
            sa.select(db.User).where(db.User.name == login_info.username)
        ).first()
        if user and user.check_password(login_info.password):
            user.session_id = login_info.session_id
            success = True
    if success:
        ui.open("/")
    else:
        ui.notify("Login Failed", type="negative")
