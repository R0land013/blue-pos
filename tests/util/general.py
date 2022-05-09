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


def get_all_sales_from_database() -> list:
    with create_test_session() as session:
        return session.query(Sale).options(joinedload(Sale.product)).all()


def get_one_sale_from_database() -> Sale:
    with create_test_session() as session:
        return session.query(Sale).options(joinedload(Sale.product)).one()


def __are_sales_equal_ignoring_id(sale_1: Sale, sale_2: Sale):
    return (sale_1.product_id == sale_2.product_id and sale_1.date == sale_2.date
            and sale_1.price == sale_2.price and sale_1.profit == sale_2.profit)


def insert_sale_and_return_it(sale: Sale):
    with create_test_session() as session:
        session.add(sale)
        session.commit()
        return sale


def assert_sale_lists_are_equal_ignoring_id(list_1: list, list_2):
    assert len(list_1) == len(list_2), 'Lists have different sizes.'

    for sale_index in range(len(list_1)):
        sale_1 = list_1[sale_index]
        sale_2 = list_2[sale_index]
        assert __are_sales_equal_ignoring_id(sale_1, sale_2), '{} != {}'.format(sale_1, sale_2)
