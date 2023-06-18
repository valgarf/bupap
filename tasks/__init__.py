from invoke import Collection

from . import docker, local, publish

ns = Collection()
ns.add_collection(Collection.from_module(docker))
ns.add_collection(Collection.from_module(local))
ns.add_collection(Collection.from_module(publish))

ns.configure({'docker': { 'target': {'build': 'all', 'run': 'debug'}}})
