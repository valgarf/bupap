from dataclasses import dataclass, field

from bupap import db
from bupap.avatar import random_avatar


@dataclass
class NewUser:
    name: str = ""
    full_name: str = ""
    password: str = ""
    avatar: str = field(default_factory=random_avatar)

    def reset(self):
        self.name = ""
        self.full_name = ""
        self.password = ""
        self.avatar = random_avatar()

    def new_random_avatar(self):
        self.avatar = random_avatar()
