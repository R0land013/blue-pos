from sqlalchemy.orm import Session, joinedload
from sqlalchemy import create_engine, select

from model.entity.models import Product, Sale

TEST_DB_URL = 'sqlite:///test.db'


def create_test_session() -> Session:
    engine = create_engine(TEST_DB_URL)
    return Session(engine, expire_on_commit=False)


def insert_product_and_return_it(product: Product) -> Product:
    """
    Insert a product into the test database, and return it. The object
    returned is not linked with a database session.

    :param Product product:
    :return Product:
    """
    with create_test_session() as session:
        session.add(product)
        session.commit()
        return product


def insert_products_in_database_and_return_them(products: list) -> list:
    with create_test_session() as session:
        session.add_all(products)
        session.commit()

        return products


def get_one_product_from_database() -> Product:
    """
    Returns the first product from the database. The object is not
    linked with a database session.

    :return Product:
    """
    with create_test_session() as session:
        return session.query(Product).options(joinedload(Product.sales)).one()


def get_all_products_in_database() -> list:
    """
    Return all products in database. The returned products are not linked
    with any database session.

    :return list:
    """

    with create_test_session() as session:

        return session.query(Product).options(joinedload(Product.sales)).all()


def delete_all_products_from_database():

    with create_test_session() as session:
        statement = select(Product)
        for a_product in session.scalars(statement):
            session.delete(a_product)
        session.commit()


def get_all_sales_from_database():
    with create_test_session() as session:
        return session.query(Sale).options(joinedload(Sale.product)).all()
