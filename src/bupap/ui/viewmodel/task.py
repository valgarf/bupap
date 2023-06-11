from dataclasses import dataclass, field
from datetime import datetime, timedelta

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
