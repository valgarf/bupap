from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Self

from bupap import db


@dataclass
class NewTask:
    project_id: int
    task_type: db.TaskType
    priority: db.TaskPriority
    created_at: datetime = field(default_factory=datetime.utcnow)
    name: str = ""
    description: str = ""
    parent_id: int | None = None
    children: list[Self] = field(default_factory=list)

    def reset(self):
        self.name = ""
        self.description = ""
        self.parent_id = None


@dataclass
class NewEstimate:
    task_id: int
    user_id: int
    estimate_type_id: int
    duration: timedelta
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class TaskDone:
    task_id: int
    finished_at: datetime = field(default_factory=datetime.utcnow)
