from functools import partial

from nicegui import ui

from bupap import db
from bupap.ui import component
from bupap.ui.component import Router


def user_card(user: db.User):
    with ui.card() as card:
        card.classes("p-4 hover:bg-slate-200")
        card.on("click", partial(Router.get().open, f"/user/{user.id}/Overview"))
        with ui.row():
            component.Avatar(user).classes("h-14")
            with ui.column().classes("gap-0 mt-2"):
                ui.label(user.full_name).classes("text-base font-bold")
                ui.label("@" + user.name).classes("text-sm text-slate-500")
    return card
