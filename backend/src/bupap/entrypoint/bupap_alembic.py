import os
import sys
from contextlib import chdir
from pathlib import Path

from alembic.config import main as alembic_main

ALEMBIC_DIR = Path(__file__).parent.parent.resolve() / "db" / "alembic"


def main():
    os.chdir(ALEMBIC_DIR)
    argv = sys.argv[1:]
    alembic_main(argv=argv, prog="bupap-alembic")


def upgrade_head():
    with chdir(ALEMBIC_DIR):
        alembic_main(argv=["upgrade", "head"], prog="bupap-alembic")


if __name__ == "__main__":
    main()
