from pathlib import Path

from invoke import task

from .helper import PROJECT_ROOT


@task
def install(ctx):
    with ctx.cd(PROJECT_ROOT):
        ctx.run("poetry install --with dev")

@task
def build(ctx):
    with ctx.cd(PROJECT_ROOT):
        ctx.run("poetry build")
