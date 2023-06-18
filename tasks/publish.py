from pathlib import Path

from invoke import task

from .docker import build as docker_build
from .helper import PROJECT_ROOT, AppInfo
from .local import build as local_build
from .local import install


@task
def tag(ctx):
    app_info = AppInfo.get(ctx)
    with ctx.cd(PROJECT_ROOT):
        ctx.run(f"git tag v{app_info.version}")

@task(install, local_build)
def poetry(ctx):
    with ctx.cd(PROJECT_ROOT):
        ctx.run("poetry publish")

@task(install, local_build, docker_build)
def docker(ctx):
    app_info = AppInfo.get(ctx)
    with ctx.cd(PROJECT_ROOT):
        ctx.run(f"docker push valgarf/bupap:{app_info.version}")
        ctx.run("docker push valgarf/bupap:latest")

@task(tag, poetry, docker, default=True)
def all(ctx):
    pass
