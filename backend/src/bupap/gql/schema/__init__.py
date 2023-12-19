import strawberry
from strawberry.schema.config import StrawberryConfig

from .mutation import Mutation
from .query import Query

schema = strawberry.Schema(
    query=Query, mutation=Mutation, config=StrawberryConfig(auto_camel_case=True)
)
