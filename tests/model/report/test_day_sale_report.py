import unittest
from datetime import date, timedelta
from model.report.day import DaySaleReport
from model.repository.factory import RepositoryFactory
from tests.util.general import TEST_DB_URL, delete_all_products_from_database, insert_product_and_return_it, \
    insert_sales_and_return_them, assert_sale_lists_are_equal_ignoring_id
from tests.util.generators.product import ProductGenerator
from tests.util.generators.sale import SaleGenerator


class TestDaySaleReport(unittest.TestCase):

    def setUp(self) -> None:
        self.sale_repository = RepositoryFactory.get_sale_repository(TEST_DB_URL)
        self.TODAY = date.today()
        self.YESTERDAY = self.TODAY - timedelta(days=1)

    def tearDown(self):
        RepositoryFactory.close_session()
        delete_all_products_from_database()

    def test_get_sales(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sales = SaleGenerator.generate_sales_from_product(product, 3)
        s1, s2, s3 = sales
        s1.date = self.YESTERDAY
        s2.date = self.TODAY
        s3.date = self.YESTERDAY
        sales = insert_sales_and_return_them(sales)

        report = DaySaleReport(self.YESTERDAY, self.sale_repository)
        sales_of_report = report.get_sales()

        assert_sale_lists_are_equal_ignoring_id(sales_of_report, [s1, s3])
