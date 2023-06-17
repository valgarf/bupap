from pathlib import Path

from invoke import task

project_root = Path(__file__).parent.parent

@task
def build(c, target="debug"):
    with c.cd(project_root):
        app_info = c.run('poetry version', hide=True).stdout.strip()
        app_version = c.run('poetry version -s', hide=True).stdout.strip()
        app_name = app_info[:-len(app_version)].strip()
        c.run(f'docker build --target {target} -t {app_name}:{target}-{app_version} -f ./docker/Dockerfile --build-arg="APP_VERSION={app_version}"  .')

@task
def run(c, target="debug"):
    app_info = c.run('poetry version', hide=True).stdout.strip()
    app_version = c.run('poetry version -s', hide=True).stdout.strip()
    app_name = app_info[:-len(app_version)].strip()
    extra = ""
    if target == "debug":
        extra +=' --mount type=bind,source=./src,target=/app/src'
    with c.cd(project_root):
        c.run(f"docker run{extra} {app_name}:{target}-{app_version} bupap", echo=True)
