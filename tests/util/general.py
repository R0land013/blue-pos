from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

from model.entity.models import Product

TEST_DB_URL = 'sqlite:///test.db'


def create_test_session() -> Session:
    engine = create_engine(TEST_DB_URL)
    return Session(engine)


def __get_unlinked_copy_of_product(product: Product) -> Product:
    product_copy = Product()
    product_copy.id = product.id
    product_copy.name = product.name
    product_copy.description = product.description
    product_copy.price = product.price
    product_copy.profit = product.profit
    product_copy.quantity = product.quantity
    return product_copy


def insert_product_and_return_it(product: Product) -> Product:
    """
    Insert a product into the test database, and return it. The object
    returned is not linked with a database session and errors will not
    be thrown when accessing a field of the object.

    :param Product product:
    :return Product:
    """
    with create_test_session() as session:
        session.add(product)
        session.commit()
        return __get_unlinked_copy_of_product(product)


def insert_products_in_database_and_return_them(products: list) -> list:
    with create_test_session() as session:
        session.add_all(products)
        session.commit()

        products_copy = list(map(__get_unlinked_copy_of_product, products))
        return products_copy


def get_one_product_from_database() -> Product:
    """
    Returns the first product from the database. The object is not
    linked with a database session.

    :return Product:
    """
    with create_test_session() as session:
        product_linked_to_session = session.scalar(select(Product))
        return __get_unlinked_copy_of_product(product_linked_to_session)


def get_all_products_in_database() -> list:
    """
    Return all products in database. The returned products are not linked
    with any database session.

    :return list:
    """

    with create_test_session() as session:

        products_linked_to_session = session.scalars(select(Product)).all()
        products_to_return = map(__get_unlinked_copy_of_product, products_linked_to_session)

        return list(products_to_return)


def delete_all_products_from_database():

    with create_test_session() as session:
        statement = select(Product)
        for a_product in session.scalars(statement):
            session.delete(a_product)
        session.commit()
