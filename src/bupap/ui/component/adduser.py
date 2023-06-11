from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import sqlalchemy as sa
from loguru import logger
from nicegui import globals, ui

from bupap import db
from bupap.avatar import random_avatar
from bupap.ui.crud.user import create_user
from bupap.ui.viewmodel.user import NewUser

from .avatar import Avatar
from .errors import Errors


class AddUser:
    def __init__(self, cb_on_create: Callable[[], None] | None = None):
        self.model = NewUser()
        self.cb_on_create = cb_on_create
        with ui.dialog() as dialog, ui.card():
            self.dialog = dialog
            self.avatar = (
                Avatar(self.model.avatar).on("click", self.set_random_avatar).classes("h-80")
            )
            ui.input(placeholder="Username").props("outline").classes("full-width").bind_value_to(
                self.model, "name"
            )
            ui.input(placeholder="Full Name").props("outline").classes("full-width").bind_value_to(
                self.model, "full_name"
            )
            ui.input(placeholder="Password").props("outline").classes("full-width").bind_value_to(
                self.model, "password"
            )
            with ui.row().classes("full-width"):
                ui.button("Create", on_click=self.create).classes("grow")
                ui.button("Cancel", on_click=self.cancel).classes("grow bg-negative")

    @Errors.wrap_error("Failed to create a user")
    def create(self):
        try:
            create_user(self.model)
        finally:
            self.model.password = ""
            self.dialog.close()
        if self.cb_on_create:
            self.cb_on_create()

    def set_random_avatar(self):
        self.model.new_random_avatar()
        self.avatar.content = self.model.avatar

    def open(self):
        self.model.reset()
        self.avatar.content = self.model.avatar
        self.dialog.open()

    def cancel(self):
        self.dialog.close()
