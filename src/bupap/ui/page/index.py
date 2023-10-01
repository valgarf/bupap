from __future__ import annotations

from functools import partial

import sqlalchemy as sa
import sqlalchemy.orm
from fastapi import Request
from fastapi.responses import RedirectResponse
from loguru import logger
from nicegui import Client, globals, ui
from starlette.middleware.sessions import SessionMiddleware

from bupap.ui.common import client_data, get_user
from bupap.ui.component import Errors, Header, RequestInfo, Router


def create_index_page():
    @ui.page("/")
    @ui.page("/{_:path}")
    def index_page(request: Request, client: Client):
        globals.index_client._custom_data = {}
        ui.add_head_html(custom_style)
        user = get_user(request)
        errors = Errors()
        router = Router(user.id)
        client_data()["router"] = router
        client.content.style("min-height: inherit")
        header = Header(user, router)

        router.frame().classes("w-full h-full grow flex flex-col flex-nowrap")

        # with ui.row().classes("absolute-center"):
        #     with ui.card():
        #         ui.label(f"Hello {user.name}!")

    @Router.add("/")
    async def index_content(info: RequestInfo, session: sa.orm.Session):
        user = Router.get().user(session)
        with ui.row().classes("absolute-center"):
            with ui.card():
                # ui.label(f"Hello {user.name}!")
                ui.label(f"Hello {user.name}")


custom_style = """
<style>
.q-expansion-item > div > .q-item {
  padding: 0;
}
.q-item >.cursor-pointer {
  padding-right: 0;
  width: 25px;
  min-width: 25px;
  align-items:center;
}
</style>
"""
