from model.repository.item import ItemRepository
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

DB_URL = 'sqlite:///data.db'


class RepositoryFactory:
    __url = None
    __session: Session = None
    __item_repository = None
    __engine = None

    @staticmethod
    def get_item_repository(url: str = DB_URL) -> ItemRepository:
        RepositoryFactory.__create_session_if_necessary(url)

        if RepositoryFactory.__item_repository is None:
            RepositoryFactory.__item_repository = ItemRepository(RepositoryFactory.__session)

        return RepositoryFactory.__item_repository

    @staticmethod
    def __create_session_if_necessary(db_url):

        if RepositoryFactory.__url != db_url:
            RepositoryFactory.__url = db_url
            RepositoryFactory.__engine = create_engine(db_url, poolclass=NullPool)
            RepositoryFactory.__session = Session(RepositoryFactory.__engine)
        return RepositoryFactory.__session

    @staticmethod
    def close_session():
        if RepositoryFactory.__session is not None:
            RepositoryFactory.__session.close()
            RepositoryFactory.__session.bind.dispose()
            RepositoryFactory.__engine.dispose()
