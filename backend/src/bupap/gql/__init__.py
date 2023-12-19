from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL

from .common.context import Context


class ContextGraphql(GraphQL):
    async def get_context(
        self, request: Request | WebSocket, response: Response | None = None
    ) -> Context:
        return Context(request, response)
