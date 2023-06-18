from pathlib import Path

from invoke import task

from .helper import PROJECT_ROOT, AppInfo, get_config
from .local import install


@task
def build(ctx, target=None):
    target = target or ctx.docker.target.build
    app_info = AppInfo.get(ctx)
    if target == "all":
        targets = ["base", "poetry-base", "debug", "release-build", "release"] #"release-test"
    else:
        targets = [target]
    with ctx.cd(PROJECT_ROOT):
        for target in targets:
            if target == "release":
                tag = app_info.version
            else:        
                tag = f"{target}-{app_info.version}"
            ctx.run(f'docker build --target {target} -t {app_info.name}:{tag} -f ./docker/Dockerfile --build-arg="APP_VERSION={app_info.version}"  .', echo = True)
            if target == "release":
                ctx.run(f'docker tag {app_info.name}:{tag} {app_info.name}:latest', echo = True)

@task(install)
def run(ctx, target=None, detach=False, bash=False, name="bupap"):
    target = target or ctx.docker.target.run
    
    extra = ""
    if target == "debug":
        extra +=' --mount type=bind,source=./src,target=/app/src'
    if detach:
        extra +=' --detach'
    else:
        extra +=' -it'
    command = ""
    if bash:
        assert not detach
        command=" bash"
    
    app_info = AppInfo.get(ctx)
    if target == "release":
        tag = app_info.version
    else:        
        tag = f"{target}-{app_info.version}"
    port = get_config(ctx,"port")
    if extra and not extra.endswith(" "):
        extra += " "
    ctx.run(f"docker stop {name}", echo=True, warn=True)
    ctx.run(f"docker container rm {name}", echo=True, warn=True)
    ctx.run(f"docker run -p {port}:80 --name {name}{extra}{app_info.name}:{tag}{command}", echo=True, pty=not detach)
