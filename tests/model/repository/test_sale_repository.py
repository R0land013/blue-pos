import unittest
from datetime import date

from model.repository.factory import RepositoryFactory
from tests.util.general import TEST_DB_URL, delete_all_products_from_database, insert_product_and_return_it, \
    get_one_product_from_database, get_all_sales_from_database
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
        sales = SaleGenerator.generate_sales_from_product(product, 3)

        for a_sale in sales:
            self.sale_repository.insert_sale(a_sale)

        retrieved_sales = get_all_sales_from_database()
        self.assertEqual(sales, retrieved_sales)

