from typing import Annotated

import sqlalchemy as sa
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

intpk = Annotated[int, mapped_column(primary_key=True, index=True)]
intfk = Annotated[int, mapped_column(index=True)]
str_10 = Annotated[str, mapped_column(sa.String(10))]
str_20 = Annotated[str, mapped_column(sa.String(20))]
str_30 = Annotated[str, mapped_column(sa.String(30))]
str_50 = Annotated[str, mapped_column(sa.String(50))]
str_60 = Annotated[str, mapped_column(sa.String(60))]
text = Annotated[str, mapped_column(sa.Text)]


class Base(sa.orm.DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__

    id: Mapped[intpk] = mapped_column()


class InheritanceBase:
    @declared_attr
    def cls_name(cls) -> Mapped[str_20]:
        return mapped_column()

    @classmethod
    def _find_toplevel_class(cls):
        return cls.__mro__[cls.__mro__.index(InheritanceBase) - 1]

    @declared_attr.directive
    def __mapper_args__(cls):
        result = {}
        toplevel_cls = cls._find_toplevel_class()
        if cls == toplevel_cls:
            result["polymorphic_on"] = "cls_name"
        else:
            result["polymorphic_load"] = "inline"

        result["polymorphic_identity"] = cls.__name__
        return result


class InheritanceFK:
    @declared_attr
    def id(cls) -> Mapped[intpk]:
        mro = [c for c in cls.__mro__ if c not in (cls, InheritanceFK)]
        parent = mro[0]
        if parent == InheritanceBase:  # Cannot use the class itself because it might be unknown
            return Base.id
        else:
            return mapped_column(sa.ForeignKey(f"{parent.__name__}.id"))
