from dependency_injector import containers, providers

from bupap import db


def db_session():
    with db.session() as session:
        yield session


class InjectDb(containers.DeclarativeContainer):
    session = providers.Resource(db_session)


class Inject(containers.DeclarativeContainer):
    db = providers.Container(InjectDb)
