import unittest
from datetime import date

from model.repository.exc.product import NonExistentProductException, NoPositivePriceException
from model.repository.exc.sale import NoEnoughProductQuantityException
from model.repository.factory import RepositoryFactory
from model.util.monetary_types import CUPMoney
from tests.util.general import TEST_DB_URL, delete_all_products_from_database, insert_product_and_return_it, \
    get_all_sales_from_database, assert_sale_lists_are_equal_ignoring_id, get_one_product_from_database
from tests.util.generators.product import ProductGenerator
from tests.util.generators.sale import SaleGenerator


class TestSaleRepository(unittest.TestCase):

    def setUp(self):
        self.sale_repository = RepositoryFactory.get_sale_repository(TEST_DB_URL)
        self.TODAY_DATE = date.today()

    def tearDown(self):
        RepositoryFactory.close_session()
        delete_all_products_from_database()

    def test_sales_are_inserted(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sale = SaleGenerator.generate_one_sale_from_product(product)

        self.sale_repository.insert_sales(sale, 3)

        inserted_sales = get_all_sales_from_database()
        correct_sales = [sale] * 3
        assert_sale_lists_are_equal_ignoring_id(inserted_sales, correct_sales)

    def test_sale_insertion_with_zero_quantity_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sale = SaleGenerator.generate_one_sale_from_product(product)

        self.assertRaises(ValueError, self.sale_repository.insert_sales, sale, 0)

    def test_sale_insertion_decreases_product_quantity(self):
        product = ProductGenerator.generate_one_product()
        product.quantity = 5
        product = insert_product_and_return_it(product)
        sale = SaleGenerator.generate_one_sale_from_product(product)

        self.sale_repository.insert_sales(sale, 3)

        product = get_one_product_from_database()
        self.assertEqual(product.quantity, 2)

    def test_sale_insertion_with_no_enough_products_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product.quantity = 2
        product = insert_product_and_return_it(product)
        sale = SaleGenerator.generate_one_sale_from_product(product)

        self.assertRaises(NoEnoughProductQuantityException, self.sale_repository.insert_sales, sale, 5)

    def test_sale_insertion_with_nonexistent_product_raises_exception(self):
        sale = SaleGenerator.generate_one_sale_without_product()
        nonexistent_product_id = 3
        sale.product_id = nonexistent_product_id

        self.assertRaises(NonExistentProductException, self.sale_repository.insert_sales, sale, 1)

    def test_sale_insertion_with_no_positive_price_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sale = SaleGenerator.generate_one_sale_from_product(product)
        sale.price = CUPMoney('0.00')

        self.assertRaises(NoPositivePriceException, self.sale_repository.insert_sales, sale, 1)
