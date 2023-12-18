from dataclasses import dataclass, field

from bupap import db


@dataclass
class NewTeam:
    name: str = ""

    def reset(self):
        self.name = ""
