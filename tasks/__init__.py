from invoke import Collection

from . import docker

ns = Collection()
ns.add_collection(Collection.from_module(docker))
