from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, Any, Callable, Mapping, Sequence, Type

import strawberry
from strawberry.extensions.field_extension import FieldExtension
from strawberry.field import StrawberryField

if TYPE_CHECKING:
    from strawberry.types import Info


def map_to_db(attr_name: str | None = None, **kwargs):
    """
    Map the field to a
    """

    def raise_resolve(root: DBType, info: Any):
        raise NotImplementedError()

    kwargs["resolver"] = raise_resolve
    kwargs["extensions"] = [DBAttrExtension(attr_name)]
    return strawberry.field(**kwargs)


class DBAttrExtension(FieldExtension):
    def __init__(self, attr_name: str | None):
        self.attr_name = attr_name

    def resolve(self, next_: Callable[..., Any], source: Any, info: Info, **kwargs):
        return getattr(source.db_obj, self.attr_name)

    def apply(self, field: StrawberryField) -> None:
        if self.attr_name is None:
            self.attr_name = field.python_name


@dataclasses.dataclass
class DBType:
    db_obj: strawberry.Private[object]
