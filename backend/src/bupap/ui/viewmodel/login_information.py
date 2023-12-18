from dataclasses import dataclass


@dataclass
class LoginInformation:
    session_id: str
    username: str = ""
    password: str = ""
