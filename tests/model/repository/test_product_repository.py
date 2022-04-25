import unittest
from model.repository.exc.product import UniqueProductNameException, NonExistentProductException, \
    InvalidProductQuantityException, InvalidPriceForProductException, NegativeProfitForProductException
from model.repository.factory import RepositoryFactory
from model.repository.product import ProductFilter
from model.util.monetary_types import CUPMoney
from tests.util.generators.product import ProductGenerator
from tests.util.general import TEST_DB_URL, get_all_products_in_database, insert_product_and_return_it, \
    get_one_product_from_database, insert_products_in_database, delete_all_products_from_database


class TestProductRepository(unittest.TestCase):

    def setUp(self):
        self.product_repository = RepositoryFactory.get_product_repository(TEST_DB_URL)

    def tearDown(self):
        RepositoryFactory.close_session()
        delete_all_products_from_database()

    def test_products_are_inserted_successfully(self):
        products = ProductGenerator.generate_products_by_quantity(3)

        for a_product in products:
            self.product_repository.insert_product(a_product)
        inserted_products = get_all_products_in_database()

        self.assertEqual(inserted_products, products)

    def test_product_inserted_with_used_name_raise_exception(self):
        product = ProductGenerator.generate_one_product()

        self.product_repository.insert_product(product)

        self.assertRaises(UniqueProductNameException, self.product_repository.insert_product, product)

    def test_product_inserted_with_used_name_in_uppercase_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        self.product_repository.insert_product(product)

        product.name = product.name.upper()

        self.assertRaises(UniqueProductNameException, self.product_repository.insert_product,
                          product)

    def test_product_inserted_with_negative_quantity_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product.quantity = -1
        self.assertRaises(InvalidProductQuantityException, self.product_repository.insert_product,
                          product)

    def test_product_inserted_with_negative_price_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product.price = CUPMoney('-1.00')

        self.assertRaises(InvalidPriceForProductException, self.product_repository.insert_product,
                          product)

    def test_product_inserted_with_zero_price_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product.price = CUPMoney('0.00')

        self.assertRaises(InvalidPriceForProductException, self.product_repository.insert_product,
                          product)

    def test_product_inserted_with_negative_profit_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product.profit = CUPMoney('-1.00')

        self.assertRaises(NegativeProfitForProductException, self.product_repository.insert_product,
                          product)

    def test_product_is_deleted_successfully(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)

        self.product_repository.delete_product(product)

        products = get_all_products_in_database()
        self.assertEqual(len(products), 0)

    def test_trying_to_delete_nonexistent_product_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product.id = 1

        self.assertRaises(NonExistentProductException, self.product_repository.delete_product,
                          product)

    def test_product_is_updated_successfully(self):
        product = ProductGenerator.generate_one_product()

        product = insert_product_and_return_it(product)
        new_product = ProductGenerator.generate_one_product()
        new_product.id = product.id

        self.product_repository.update_product(new_product)

        updated_product = get_one_product_from_database()
        self.assertEqual(updated_product, new_product)

    def test_trying_to_update_nonexistent_product_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product.id = 1

        new_product = ProductGenerator.generate_one_product()
        new_product.id = product.id

        self.assertRaises(NonExistentProductException, self.product_repository.update_product,
                          new_product)

    def test_trying_to_update_product_using_existent_name_raises_exception(self):
        first_product, second_product = ProductGenerator.generate_products_by_quantity(2)
        first_product = insert_product_and_return_it(first_product)
        second_product = insert_product_and_return_it(second_product)

        new_product = ProductGenerator.generate_one_product()
        new_product.id = first_product.id
        new_product.name = second_product.name

        self.assertRaises(UniqueProductNameException, self.product_repository.update_product,
                          new_product)

    def test_trying_to_update_product_using_same_name_does_not_raise_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        new_product = ProductGenerator.generate_one_product()
        new_product.id = product.id
        new_product.name = product.name

        self.product_repository.update_product(new_product)

        updated_product = get_one_product_from_database()
        self.assertEqual(updated_product, new_product)

    def test_product_updated_with_negative_quantity_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        product.quantity = -1

        self.assertRaises(InvalidProductQuantityException, self.product_repository.update_product,
                          product)

    def test_product_updated_with_negative_price_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        product.price = CUPMoney('-1.00')

        self.assertRaises(InvalidPriceForProductException, self.product_repository.update_product,
                          product)

    def test_product_updated_with_zero_price_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        product.price = CUPMoney('0.00')

        self.assertRaises(InvalidPriceForProductException, self.product_repository.update_product,
                          product)

    def test_product_updated_with_negative_profit_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        product.profit = CUPMoney('-1.00')

        self.assertRaises(NegativeProfitForProductException, self.product_repository.update_product,
                          product)

    def test_get_all_products_returns_empty_list(self):
        empty_list = []

        retrieved_list = self.product_repository.get_all_products()

        self.assertEqual(retrieved_list, empty_list)

    def test_get_all_products_returns_nonempty_list(self):
        products = ProductGenerator.generate_products_by_quantity(3)
        insert_products_in_database(products)
        products = get_all_products_in_database()

        retrieved_products = self.product_repository.get_all_products()
        self.assertEqual(products, retrieved_products)

    def test_get_products_by_filter_id(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        the_filter = ProductFilter()
        the_filter.id = product.id

        filtered_product = self.product_repository.get_products_by_filter(the_filter)

        self.assertEqual(product, filtered_product)
