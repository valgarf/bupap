from pathlib import Path

from invoke import task

project_root = Path(__file__).parent.parent

@task
def install(ctx):
    with ctx.cd(project_root):
        ctx.run("poetry install --with dev")

