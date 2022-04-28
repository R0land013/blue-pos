import unittest
from datetime import date

from model.repository.factory import RepositoryFactory
from tests.util.general import TEST_DB_URL, delete_all_products_from_database, insert_product_and_return_it, \
    get_one_product_from_database, get_all_sales_from_database
from tests.util.generators.product import ProductGenerator


class TestSaleRepository(unittest.TestCase):

    def setUp(self):
        self.sale_repository = RepositoryFactory.get_sale_repository(TEST_DB_URL)
        self.TODAY_DATE = date.today()

    def tearDown(self):
        RepositoryFactory.close_session()
        delete_all_products_from_database()

    def test_sale_is_inserted(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)

        self.sale_repository.insert_sale(product, self.TODAY_DATE)

        product = get_one_product_from_database()
        inserted_sales = get_all_sales_from_database()
        self.assertEqual(product.sales, inserted_sales)
