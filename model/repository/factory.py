from model.repository.expense import ExpenseRepository
from model.repository.product import ProductRepository
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from model.repository.sale import SaleRepository
from model.repository.sales_grouped_by_product import SalesGroupedByProductRepository

DB_URL = 'sqlite:///data.db?check_same_thread=False'


class RepositoryFactory:
    __url = None
    __session: Session = None
    __product_repository = None
    __sale_repository = None
    __sales_grouped_by_product_repository = None
    __expense_repository = None
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
    def get_sale_repository(url: str = DB_URL) -> SaleRepository:
        RepositoryFactory.__create_session_if_necessary(url)

        if RepositoryFactory.__sale_repository is None:
            RepositoryFactory.__sale_repository = SaleRepository(RepositoryFactory.__session)

        return RepositoryFactory.__sale_repository

    @staticmethod
    def get_expense_repository(url: str = DB_URL) -> ExpenseRepository:
        RepositoryFactory.__create_session_if_necessary(url)

        if RepositoryFactory.__expense_repository is None:
            RepositoryFactory.__expense_repository = ExpenseRepository(RepositoryFactory.__session)

        return RepositoryFactory.__expense_repository

    @staticmethod
    def get_sales_grouped_by_product_repository(url: str = DB_URL) -> SalesGroupedByProductRepository:
        RepositoryFactory.__create_session_if_necessary(url)

        if RepositoryFactory.__sales_grouped_by_product_repository is None:
            RepositoryFactory.__sales_grouped_by_product_repository = SalesGroupedByProductRepository(
                RepositoryFactory.__session)

        return RepositoryFactory.__sales_grouped_by_product_repository

    @staticmethod
    def close_session():
        if RepositoryFactory.__session is not None:
            RepositoryFactory.__session.close()
            RepositoryFactory.__session.bind.dispose()
            RepositoryFactory.__engine.dispose()
