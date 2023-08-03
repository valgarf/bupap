from asyncio import iscoroutinefunction
from functools import wraps
from inspect import isawaitable
from traceback import format_tb
from typing import Callable, Optional, Self

from loguru import logger
from nicegui import ui

from bupap.ui.common import client_data


class Errors(ui.element, component="errors.js"):
    def __init__(self) -> None:
        super().__init__()
        self.on("show_full_error", self.show_full_error)
        client_data()["errors"] = self

    @classmethod
    def get(cls) -> Self:
        return client_data()["errors"]

    def show_error(self, shortmsg: str | None = None, exc: Exception | None = None) -> None:
        assert shortmsg or exc
        if not shortmsg:
            shortmsg = "Internal Error"
        traceback = ""
        if exc is not None:
            traceback = "".join(format_tb(exc.__traceback__))
        msg = ""
        if exc:
            msg = str(exc)
            if hasattr(exc, "detail"):
                if msg:
                    msg += f" ({exc.detail})"
                else:
                    msg = exc.detail
        self.run_method(
            "show_short_error", shortmsg, type(exc).__name__ if exc else "", msg, traceback,
        )

    def show_full_error(self, evt):
        short_msg = evt.args["short_msg"]
        exc_type = evt.args["exc_type"]
        exc_msg = evt.args["exc_msg"]
        traceback = evt.args["traceback"]
        with ui.dialog() as dialog, ui.card() as card:
            card.classes("flex-nowrap").style("max-width:80%!important; width:80%!important")
            with ui.row():
                ui.icon("error", color="negative", size="lg")
                with ui.column():
                    ui.label(short_msg).classes("font-bold")
                    if exc_type and exc_msg:
                        ui.label(f"{exc_type}: {exc_msg}")
                    elif exc_type:
                        ui.label(f"{exc_type}")
                    elif exc_msg:
                        ui.label(f"{exc_msg}")
            if traceback:
                with ui.expansion("Traceback:").classes("w-full"):
                    ui.markdown(f"```\n{traceback}```" "").classes("w-full overflow-auto")
            with ui.row().classes("full-width justify-center"):
                ui.button("Close", on_click=dialog.close).classes("bg-negative")
        dialog.open()

    @classmethod
    def wrap_error(cls, shortmsg: str | None, reraise: bool = False):
        def decorator(f):
            if iscoroutinefunction(f):

                @wraps(f)
                async def wrapper(*args, **kwargs):
                    try:
                        return await f(*args, **kwargs)
                    except Exception as exc:
                        # Remove this wrapper from the traceback, it is not relevant
                        if exc.__traceback__ is not None and exc.__traceback__.tb_next is not None:
                            exc.__traceback__ = exc.__traceback__.tb_next
                        Errors.get().show_error(shortmsg, exc)
                        if reraise:
                            raise

            else:

                @wraps(f)
                def wrapper(*args, **kwargs):
                    try:
                        return f(*args, **kwargs)
                    except Exception as exc:
                        # Remove this wrapper from the traceback, it is not relevant
                        if exc.__traceback__ is not None and exc.__traceback__.tb_next is not None:
                            exc.__traceback__ = exc.__traceback__.tb_next
                        Errors.get().show_error(shortmsg, exc)
                        if reraise:
                            raise

            return wrapper

        return decorator


# ["2de1c2","f25757","63474d","d4b2d8","edae49"]
