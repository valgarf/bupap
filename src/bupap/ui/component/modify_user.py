from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import sqlalchemy as sa
from loguru import logger
from nicegui import globals, ui

from bupap import db
from bupap.avatar import deserialize_avatar, random_avatar
from bupap.ui.crud.user import update_user
from bupap.ui.viewmodel.user import ModifiedUser

from .avatar import Avatar
from .errors import Errors


class ModifyUser:
    def __init__(self, user: db.User, cb_on_modify: Callable[[], None] | None = None):
        self.model = ModifiedUser(
            db_id=user.id,
            name=user.name,
            full_name=user.full_name,
            avatar=deserialize_avatar(user.avatar),
        )
        self.cb_on_modify = cb_on_modify
        with ui.dialog() as self.dialog, ui.card():
            self.avatar = (
                Avatar(self.model.avatar).on("click", self.set_random_avatar).classes("h-80")
            )
            ui.input(placeholder="Username").props("outline").classes("full-width").bind_value(
                self.model, "name"
            )
            ui.input(placeholder="Full Name").props("outline").classes("full-width").bind_value(
                self.model, "full_name"
            )
            with ui.row().classes("full-width"):
                ui.button("Save", on_click=self.save).classes("grow")
                ui.button("Cancel", on_click=self.cancel).classes("grow bg-negative")

    @Errors.wrap_error("Failed to create a user")
    def save(self):
        try:
            update_user(self.model)
        finally:
            self.dialog.close()
        if self.cb_on_modify:
            self.cb_on_modify()

    def set_random_avatar(self):
        self.model.new_random_avatar()
        self.avatar.value = self.model.avatar

    def open(self):
        self.avatar.value = self.model.avatar
        self.dialog.open()

    def cancel(self):
        self.dialog.close()
