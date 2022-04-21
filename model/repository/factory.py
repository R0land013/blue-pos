from model.repository.product import ProductRepository
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

DB_URL = 'sqlite:///data.db'


class RepositoryFactory:
    __url = None
    __session: Session = None
    __product_repository = None
    __engine = None

    @staticmethod
    def get_product_repository(url: str = DB_URL) -> ProductRepository:
        RepositoryFactory.__create_session_if_necessary(url)

        if RepositoryFactory.__product_repository is None:
            RepositoryFactory.__product_repository = ProductRepository(RepositoryFactory.__session)

        return RepositoryFactory.__product_repository

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
