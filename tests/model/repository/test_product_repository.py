import unittest
from sqlalchemy import select
from model.entity.models import Product
from model.repository.exc.product import UniqueProductNameException, NonExistentProductException, \
    InvalidProductQuantityException
from model.repository.factory import RepositoryFactory
from tests.util.generators.product import ProductGenerator
from tests.util.general import TEST_DB_URL
from tests.util.general import create_test_session


class TestProductRepository(unittest.TestCase):

    def setUp(self):
        self.product_repository = RepositoryFactory.get_product_repository(TEST_DB_URL)

    def tearDown(self):
        RepositoryFactory.close_session()

        with create_test_session() as session:
            statement = select(Product)
            for an_product in session.scalars(statement):
                session.delete(an_product)
            session.commit()

    def test_products_are_inserted_successfully(self):
        fake_products = ProductGenerator.generate_products_by_quantity(3)

        for an_product in fake_products:
            self.product_repository.insert_product(an_product)

        with create_test_session() as session:
            inserted_products = session.scalars(select(Product)).all()
            self.assertEqual(inserted_products, fake_products)

    def test_product_inserted_with_used_name_raise_exception(self):
        fake_product = ProductGenerator.generate_one_product()

        self.product_repository.insert_product(fake_product)

        self.assertRaises(UniqueProductNameException, self.product_repository.insert_product, fake_product)

    def test_product_inserted_with_used_name_in_uppercase_raises_exception(self):
        fake_product = ProductGenerator.generate_one_product()
        self.product_repository.insert_product(fake_product)

        fake_product.name = fake_product.name.upper()

        self.assertRaises(UniqueProductNameException, self.product_repository.insert_product,
                          fake_product)

    def test_product_inserted_with_negative_quantity_raises_exception(self):
        fake_product = ProductGenerator.generate_one_product()
        fake_product.quantity = -1
        self.assertRaises(InvalidProductQuantityException, self.product_repository.insert_product,
                          fake_product)

    def test_product_is_deleted_successfully(self):
        fake_product = ProductGenerator.generate_one_product()
        with create_test_session() as session:
            session.add(fake_product)
            session.commit()

        with create_test_session() as session:
            fake_product = session.scalar(select(Product))
            self.product_repository.delete_product(fake_product)

            products = session.scalars(select(Product)).all()
            self.assertEqual(len(products), 0)

    def test_trying_to_delete_nonexistent_product_raises_exception(self):
        fake_product = ProductGenerator.generate_one_product()
        fake_product.id = 1

        self.assertRaises(NonExistentProductException, self.product_repository.delete_product,
                          fake_product)

    def test_product_is_updated_successfully(self):
        fake_product = ProductGenerator.generate_one_product()

        with create_test_session() as session:
            session.add(fake_product)
            session.commit()
            new_product = ProductGenerator.generate_one_product()
            new_product.id = fake_product.id

            self.product_repository.update_product(new_product)

            session.expunge_all()
            updated_product = session.scalar(select(Product))
            self.assertEqual(updated_product, new_product)

    def test_trying_to_update_nonexistent_product_raises_exception(self):
        fake_product = ProductGenerator.generate_one_product()
        fake_product.id = 1

        new_product = ProductGenerator.generate_one_product()
        new_product.id = fake_product.id

        self.assertRaises(NonExistentProductException, self.product_repository.update_product,
                          new_product)

    def test_trying_to_update_product_using_existent_name_raises_exception(self):
        first_product, second_product = ProductGenerator.generate_products_by_quantity(2)

        with create_test_session() as session:
            session.add_all([first_product, second_product])
            session.commit()

            new_product = ProductGenerator.generate_one_product()
            new_product.id = first_product.id
            new_product.name = second_product.name

            self.assertRaises(UniqueProductNameException, self.product_repository.update_product,
                              new_product)

    def test_trying_to_update_product_using_same_name_does_not_raise_exception(self):
        fake_product = ProductGenerator.generate_one_product()

        with create_test_session() as session:
            session.add(fake_product)
            session.commit()
            new_product = ProductGenerator.generate_one_product()
            new_product.id = fake_product.id
            new_product.name = fake_product.name

            self.product_repository.update_product(new_product)

            session.expunge_all()
            updated_product = session.scalar(select(Product))
            self.assertEqual(updated_product, new_product)

    def test_product_updated_with_negative_quantity_raises_exception(self):
        fake_product = ProductGenerator.generate_one_product()
        fake_product.quantity = -1
        with create_test_session() as session:
            session.add(fake_product)
            session.commit()

            self.assertRaises(InvalidProductQuantityException, self.product_repository.update_product,
                              fake_product)

    def test_get_all_products_returns_empty_list(self):
        empty_list = []

        retrieved_list = self.product_repository.get_all_products()

        self.assertEqual(retrieved_list, empty_list)

    def test_get_all_products_returns_nonempty_list(self):
        fake_products = ProductGenerator.generate_products_by_quantity(3)

        with create_test_session() as session:
            session.add_all(fake_products)
            session.commit()

            retrieved_products = self.product_repository.get_all_products()
            self.assertEqual(fake_products, retrieved_products)
