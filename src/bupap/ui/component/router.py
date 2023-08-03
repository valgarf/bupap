# Adapted from nicegui documentation: https://github.com/zauberzeug/nicegui/blob/main/examples/single_page_app/router.py

from __future__ import annotations

import inspect
from contextlib import ExitStack
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict, Self, Union
from urllib.parse import parse_qs, urlencode

from loguru import logger
from nicegui import background_tasks, ui
from starlette import routing

from bupap import db
from bupap.ui.common import client_data

from .errors import Errors


def _to_js(data):
    if isinstance(data, str):
        return f'"{data}"'
    if isinstance(data, (int, float)):
        return data
    if isinstance(data, list):
        return "[" + ",".join(_to_js(el) for el in data) + "]"
    if isinstance(data, dict):
        return "{" + ",".join(f"{key!s}: {_to_js(value)}" for key, value in data.items()) + "}"


@dataclass
class RequestInfo:
    params: Dict[str, Any]
    query_data: Dict[str, Any]

class RouterFrame(ui.element, component="router.js"):
    pass

class Router:
    routes: list[routing.Route] = []

    def __init__(self, user_id: str) -> None:
        self.content: ui.element = None
        self.user_id = user_id
        self.last_path = None
        self.last_query_data = None
        client_data()["router"] = self

    @classmethod
    def get(cls) -> Self:
        return client_data()["router"]

    @classmethod
    def add(cls, path: str):
        def decorator(func: Callable):
            cls.routes.append(routing.Route(path, func, methods=["GET"]))
            return func

        return decorator

    @Errors.wrap_error("Failed to open page")
    def open(self, path: str, query_data: Union[str, dict] = "", push_state=True):
        # print(path, query_data, push_state)
        assert isinstance(path, str)
        scope = {"method": "GET", "type": "http", "path": path}
        child_scope = None
        for r in self.routes:
            m, child_scope = r.matches(scope)
            if m == routing.Match.FULL:
                break
        else:
            raise RuntimeError(f"Could not resolve route {path}")
        builder = child_scope["endpoint"]
        parameters = {p.name for p in inspect.signature(builder).parameters.values()}

        if isinstance(query_data, str):
            query_data = parse_qs(query_data[1:])

        info = RequestInfo(params=child_scope["path_params"], query_data=query_data)

        @Errors.wrap_error("Failed to open page")
        async def build():
            try:
                with self.content:
                    self.content.clear()
                    self.last_path = path
                    self.last_query_data = query_data
                    if push_state:
                        await self.push_history(path, query_data)

                    with ExitStack() as stack:
                        kwargs = {}
                        if "session" in parameters:
                            kwargs["session"] = stack.enter_context(db.session())
                        result = builder(info, **kwargs)
                        if isinstance(result, Awaitable):
                            await result
            except Exception as exc:
                logger.opt(exception=exc).error(f"Exception during creation of page {path}:")
                raise

        # self.content.clear()
        background_tasks.create(build())

    async def push_history(self, path: str, query_data: dict):
        logger.info(f"push history: {path=}, {query_data=}")
        self.last_path = path
        self.last_query_data = query_data
        query_data_encoded = "?" + urlencode(query_data, doseq=True)
        state = {"page": path, "query_data": query_data_encoded}
        await ui.run_javascript(
            f'history.pushState({_to_js(state)}, "", {_to_js(path+query_data_encoded)})',
            respond=False,
        )

    def reload(self):
        self.open(self.last_path, self.last_query_data, push_state=False)

    def frame(self) -> ui.element:
        def open_from_browser(msg):
            logger.info(msg)
            self.open(
                msg.args["page"], msg.args["query_data"], push_state=msg.args["push_state"]
            )

        self.content = RouterFrame().on("open", open_from_browser)
        return self.content

    def user(self, session):
        return session.get(db.User, self.user_id)

    @staticmethod
    async def tab_transition_event(evt_data):
        new_tab = evt_data.args[0]
        await Router.push_history_callable(path_last_part=new_tab)()

    @staticmethod
    def push_history_callable(
        path_last_part: str | None = None,
        query_data_update: dict | None = None,
        filter_identical: bool = True,
    ):
        async def push_history_event_callable(*args, **kwargs):
            router = Router.get()
            data = dict(router.last_query_data)
            path = router.last_path
            if path_last_part:
                # replace last part of the path with new value (e.g. path/to/user/1 -> path/to/user/5)
                path = "/".join(path.split("/")[:-1] + [path_last_part])
            if query_data_update:
                data.update(query_data_update)
            if not filter_identical or path != router.last_path or data != router.last_query_data:
                await router.push_history(path, data)

        return push_history_event_callable
