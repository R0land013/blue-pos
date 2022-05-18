import unittest
from datetime import date, timedelta
from pathlib import Path

from model.report.day import DaySaleReport
from model.repository.factory import RepositoryFactory
from tests.util.general import TEST_DB_URL, delete_all_products_from_database, insert_product_and_return_it, \
    insert_sales_and_return_them, assert_sale_lists_are_equal_ignoring_id
from tests.util.generators.product import ProductGenerator
from tests.util.generators.sale import SaleGenerator


class TestDaySaleReport(unittest.TestCase):

    html_report_path = './generated/day_report.html'
    generated_directory = './generated'

    @staticmethod
    def setUpClass():
        generated_files_path = Path(TestDaySaleReport.generated_directory)
        if not generated_files_path.exists():
            generated_files_path.mkdir()

        html_day_report_path = Path(TestDaySaleReport.html_report_path)
        if html_day_report_path.exists():
            html_day_report_path.unlink()

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

    def test_html_day_report_is_generated(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sales = SaleGenerator.generate_sales_from_product(product, 3)
        s1, s2, s3 = sales
        s1.date = self.TODAY
        s2.date = self.YESTERDAY
        s3.date = self.TODAY

        report = DaySaleReport(self.TODAY, self.sale_repository)
        report_path = Path(TestDaySaleReport.html_report_path)
        report.generate_report_as_html(report_path)

        self.assertTrue(report_path.exists())
