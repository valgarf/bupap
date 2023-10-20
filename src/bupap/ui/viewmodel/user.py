from dataclasses import dataclass, field

import python_avatars as pa

from bupap import db
from bupap.avatar import random_avatar


@dataclass
class NewUser:
    name: str = ""
    full_name: str = ""
    password: str = ""
    avatar: pa.Avatar = field(default_factory=random_avatar)

    def reset(self):
        self.name = ""
        self.full_name = ""
        self.password = ""
        self.avatar = random_avatar()

    def new_random_avatar(self):
        self.avatar = random_avatar()


@dataclass
class ModifiedUser:
    db_id: str
    name: str
    full_name: str
    avatar: pa.Avatar

    def new_random_avatar(self):
        self.avatar = random_avatar()
