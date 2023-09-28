from dataclasses import dataclass, field

from bupap import db


@dataclass
class NewProject:
    name: str = ""
    description: str = ""
    color: str = ""
    parent_id: int | None = None

    def reset(self):
        self.name = ""
        self.description = ""
        self.color = ""
