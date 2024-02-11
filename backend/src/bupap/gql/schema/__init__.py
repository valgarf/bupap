import strawberry
from strawberry.schema.config import StrawberryConfig

from .mutation import Mutation
from .query import Query
from .task import (
    TaskActivityCreated,
    TaskActivityEstimateAdded,
    TaskActivityFinished,
    TaskActivityWorkperiod,
)

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    config=StrawberryConfig(auto_camel_case=True),
    types=[
        # interface implementations not used directly as return type
        TaskActivityCreated,
        TaskActivityFinished,
        TaskActivityEstimateAdded,
        TaskActivityWorkperiod,
    ],
)
