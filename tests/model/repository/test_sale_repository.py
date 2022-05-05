import unittest
from datetime import date

from model.repository.factory import RepositoryFactory
from tests.util.general import TEST_DB_URL, delete_all_products_from_database, insert_product_and_return_it, \
    get_one_product_from_database, get_all_sales_from_database, assert_sale_lists_are_equal_ignoring_id
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

