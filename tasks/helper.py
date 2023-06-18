from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

@dataclass
class AppInfo:
    name: str
    version: str

    _instance = None
    @classmethod
    def get(cls, ctx):
        if cls._instance is None:
            with ctx.cd(PROJECT_ROOT):
                app_info: str = ctx.run('poetry version', hide=True).stdout.strip()
                cls._instance = cls(*[el.strip() for el in app_info.rsplit(maxsplit=1)])
        return cls._instance
    
def get_config(ctx, key):
    """ 
    Requires the package to be installed locally!
    """
    with ctx.cd(PROJECT_ROOT):
        return ctx.run(f"poetry run bupap-settings {key}", hide=True).stdout.strip()
