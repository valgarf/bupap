from typing import Self

import strawberry

from bupap import db

from ..common.db_type import DBConvExtension, DBType, map_to_db
from .tag import Tag
from .task import Task


@strawberry.type
class Project(DBType, strawberry.relay.Node):
    _db_table = db.Project
    db_id: int = map_to_db("id")
    name: str = map_to_db()
    parent: Self | None = map_to_db()
    tasks: list[Task] = map_to_db()

    @strawberry.field()
    def children(self, recursive: bool = False) -> list[Self]:
        db_self: db.Project = self.db_obj
        if recursive:
            result = list(db_self.recursive_children)
        else:
            result = list(db_self.children)
        return [Project(db_child) for db_child in result]

    @strawberry.field()
    def parents(self) -> list[Self]:
        result = []
        p = self.db_obj.parent
        while p != None:
            result.append(Project(p))
            p = p.parent
        return result

    @strawberry.field()
    def priorities(self) -> list[Tag]:
        result = []
        for prio in db.TaskPriority:
            result.append(
                Tag(
                    key=prio.name,
                    text=prio.text,
                    color=prio.default_color,
                )
            )
        return result
