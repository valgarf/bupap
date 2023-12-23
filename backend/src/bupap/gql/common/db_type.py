from __future__ import annotations

import dataclasses
import inspect
from functools import cached_property, lru_cache
from types import UnionType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Iterable,
    Mapping,
    Self,
    Sequence,
    Type,
    Union,
    get_args,
    get_origin,
)

import sqlalchemy as sa
import strawberry
from strawberry.extensions.field_extension import FieldExtension
from strawberry.field import StrawberryField
from strawberry.lazy_type import LazyType
from strawberry.type import StrawberryList, StrawberryOptional

if TYPE_CHECKING:
    from strawberry.types import Info

    from .context import InfoContext


def map_to_db(attr_name: str | None = None, **kwargs):
    """
    Map the field to a database attribute / relationship
    """

    # we do not directly create a resolver, attr_name might be empty. Instead the DBAttrExtension
    # will use the parsed field to get an attribute name (if none is given as input).
    def raise_resolve(root: DBType, info: Any):
        raise NotImplementedError()

    kwargs["resolver"] = raise_resolve

    kwargs["extensions"] = [DBAttrExtension(attr_name), DBConvExtension()] + kwargs.get(
        "extensions", []
    )
    return strawberry.field(**kwargs)


class DBAttrExtension(FieldExtension):
    def __init__(self, attr_name: str | None):
        self.attr_name = attr_name

    def resolve(self, next_: Callable[..., Any], source: Any, info: Info, **kwargs):
        return getattr(source.db_obj, self.attr_name)

    def apply(self, field: StrawberryField) -> None:
        if self.attr_name is None:
            self.attr_name = field.python_name


@lru_cache(maxsize=1024)
def resolve_lazy_type(type_: LazyType) -> Type:
    return type_.resolve_type()


class DBConvExtension(FieldExtension):
    def __init__(self, converter: Callable[[Any], Any] | None = None):
        self.converter = None

    @cached_property
    def resolved_type(self):
        return self.field.type_annotation.resolve()

    def convert(self, type_, result):
        try:
            if result is None:
                return None
            if isinstance(type_, LazyType):
                type_ = resolve_lazy_type(type_)
            if isinstance(type_, StrawberryOptional):
                return self.convert(type_.of_type, result)
            if isinstance(type_, StrawberryList):
                if not isinstance(result, (list, tuple)):
                    raise RuntimeError(f"Expected a list for field {self.field}. Value: {result}")
                return [self.convert(type_.of_type, el) for el in result]
            if not isinstance(type_, strawberry.custom_scalar.ScalarWrapper) and issubclass(
                type_, DBType
            ):
                result = type_(result)
            return result
        except Exception as exc:
            raise

    def resolve(self, next_: Callable[..., Any], source: Any, info: Info, **kwargs):
        result = next_(source, info, **kwargs)
        if self.converter is not None:
            result = self.converter(result)
        elif self.field.type_annotation is not None:
            result = self.convert(self.resolved_type, result)
        return result

    async def resolve_async(self, next_: Callable[..., Any], source: Any, info: Info, **kwargs):
        result = next_(source, info, **kwargs)
        if inspect.isawaitable(result):
            result = await result
        if self.converter is not None:
            result = self.converter(result)
        elif self.field.type_annotation is not None:
            result = self.convert(self.resolved_type, result)
        return result

    def apply(self, field: StrawberryField) -> None:
        self.field = field
        # TODO: analyze type and disable conversion for scalar types?


@dataclasses.dataclass
class DBType:
    db_obj: strawberry.Private[object]

    @classmethod
    def resolve_id(cls, root: Self, *, info: Info) -> str:
        return str(root.db_obj.id)

    @classmethod
    def resolve_nodes(
        cls,
        *,
        info: InfoContext,
        node_ids: Iterable[str],
        required: bool = False,
    ):
        session = info.context.db_session
        int_ids = [int(nid) for nid in node_ids]
        db_query = sa.select(cls._db_table).where(cls._db_table.id.in_(int_ids))
        result = session.scalars(db_query).all()
        if len(result) != len(node_ids) and required:
            missing = set(int_ids) - {obj.id for obj in result}
            raise KeyError(f"Node ids missing for class {cls.__name__}: {missing}")
        return [cls(obj) for obj in result]
