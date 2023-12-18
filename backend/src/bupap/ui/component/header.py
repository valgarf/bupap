from functools import partial

from nicegui import ui

from bupap import db

from .router import Router


class Header:
    def __init__(self, user: db.User, router: Router):
        with ui.header(bordered=True).classes("items-center justify-between"):
            with ui.row():
                ui.button(on_click=lambda: router.open("/")).classes("q-btn--flat").props(
                    "icon=home"
                ).tooltip("Home")
                ui.button(on_click=lambda: router.open("/teams"), text="Teams").classes(
                    "q-btn--flat"
                )  # .props('icon=people')
                ui.button(on_click=lambda: router.open("/users"), text="Users").classes(
                    "q-btn--flat"
                )  # .props('icon=people')
                ui.button(on_click=lambda: router.open("/projects"), text="Projects").classes(
                    "q-btn--flat"
                )  # .props('icon=people')
            with ui.row():
                ui.button().classes("q-btn--flat").props("icon=admin_panel_settings").tooltip(
                    "Administration Settings"
                )
                ui.button().classes("q-btn--flat").props("icon=settings").tooltip("User Settings")
                ui.button(on_click=partial(logout, user.id)).classes("q-btn--flat").props(
                    "icon=logout"
                ).tooltip("Logout")


def logout(user_id):
    with db.session() as session:
        user = session.get(db.User, user_id)
        user.session_id = None
    ui.open("/login")
