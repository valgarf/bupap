from __future__ import annotations

import dataclasses
from types import UnionType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Mapping,
    Sequence,
    Type,
    Union,
    get_args,
    get_origin,
)

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
    def __init__(self, attr_name: str | None, converter: Callable[[Any], Any] | None = None):
        self.attr_name = attr_name
        self.converter = None

    def resolve(self, next_: Callable[..., Any], source: Any, info: Info, **kwargs):
        result = getattr(source.db_obj, self.attr_name)
        if self.converter is not None:
            result = self.converter(result)
        return result

    def apply(self, field: StrawberryField) -> None:
        if self.attr_name is None:
            self.attr_name = field.python_name
        if self.converter is None and field.type_annotation is not None:
            # TODO: this only works for some cases:
            # - DBObject type
            # - Optional DBObject type
            # - list of DBObject type
            anno = field.type_annotation.annotation
            if isinstance(anno, str):
                raise RuntimeError(f"Unresolved type {anno}")
            else:
                origin = get_origin(anno)
                if origin is not None:
                    if origin is UnionType:
                        args = get_args(anno)
                        if len(args) == 2 and type(None) in args:
                            # optional result
                            anno = [a for a in args if a is not None][0]
                            if issubclass(anno, DBType):

                                def converter(db_obj):
                                    if db_obj is None:
                                        return None
                                    return anno(db_obj)

                                self.converter = converter
                    elif origin is list:
                        anno = get_args(anno)[0]

                        def converter(db_objs):
                            return [anno(db_obj) for db_obj in db_objs]

                        self.converter = converter
                elif issubclass(anno, DBType):

                    def converter(db_obj):
                        return anno(db_obj)

                    self.converter = converter


@dataclasses.dataclass
class DBType:
    db_obj: strawberry.Private[object]
