from nicegui import ui

from bupap import db


class Avatar(ui.html):
    def __init__(self, user_or_avatar: db.User | str | None = None):
        # return ui.html('<svg><g transform="scale(0.2)">'+user.avatar+'</g></svg>')
        avatar_svg = ""
        if user_or_avatar and isinstance(user_or_avatar, db.User):
            avatar_svg = user_or_avatar.avatar
        elif user_or_avatar:
            avatar_svg = user_or_avatar
        super().__init__(avatar_svg)
