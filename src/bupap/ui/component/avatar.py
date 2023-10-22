from typing import Callable, Self

import python_avatars as pa
from nicegui import ui

from bupap import db
from bupap.avatar import deserialize_avatar


class Avatar(ui.html):
    def __init__(
        self,
        user_or_avatar: db.User | pa.Avatar | str | None = None,
        on_update_content: Callable[[Self], None] | None = None,
    ):
        # return ui.html('<svg><g transform="scale(0.2)">'+user.avatar+'</g></svg>')
        self.on_update_content = on_update_content
        self._value = None
        if user_or_avatar and isinstance(user_or_avatar, db.User):
            self._value = deserialize_avatar(user_or_avatar.avatar)
        elif user_or_avatar and isinstance(user_or_avatar, str):
            self._value = deserialize_avatar(user_or_avatar)
        elif user_or_avatar and isinstance(user_or_avatar, pa.Avatar):
            self._value = user_or_avatar

        if self._value is not None:
            super().__init__(self._value.render())
        else:
            super().__init__("")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, avatar: pa.Avatar):
        self._value = avatar
        self.update_content()

    def update_content(self):
        self.content = self._value.render()
        if self.on_update_content is not None:
            self.on_update_content(self)
