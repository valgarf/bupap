import os
import shutil
from pathlib import Path

from appdirs import user_config_dir, user_data_dir
from dynaconf import Dynaconf, Validator

config_dir = Path(user_config_dir("bupap"))
settings_files = [
    (Path(__file__).parent / "settings_default.toml").resolve(),
    config_dir / "settings.toml",
    config_dir / ".secrets.toml",
    "settings.toml",
    ".secrets.toml",
]

if not "BUPAP_ENV" in os.environ:
    os.environ["BUPAP_ENV"] = "testing"
    # TODO: remove me, makes 'testing' the default environment

settings = Dynaconf(
    envvar_prefix="BUPAP",
    env_switcher="BUPAP_ENV",
    merge_enable=True,
    root_path=Path().resolve(),
    settings_files=settings_files,
    environments=True,
    validators=[
        Validator("initial_admin_password", default=None),
        Validator("editable", default=(Path(__file__).parent / "data" / "EDITABLE_TAG").exists()),
        Validator("pkg_root", default=str(Path(__file__).parent)),
        Validator("user_data_dir", default=user_data_dir("bupap")),
        Validator("cwd", default=str(Path().resolve())),
    ],
)
