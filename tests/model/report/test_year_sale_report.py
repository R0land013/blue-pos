from datetime import date, timedelta
from unittest import TestCase

from model.report.year import YearSaleReport
from model.repository.factory import RepositoryFactory
from tests.util.general import TEST_DB_URL, TEST_REPORT_PATH, delete_all_products_from_database, \
    insert_product_and_return_it, insert_sales_and_return_them
from tests.util.generators.product import ProductGenerator
from tests.util.generators.sale import SaleGenerator


class TestYearSaleReport(TestCase):

    def setUp(self):
        self.sale_repository = RepositoryFactory.get_sale_repository(TEST_DB_URL)
        self.FIRST_DATE_OF_THIS_YEAR = date(day=1, month=1, year=date.today().year)
        self.LAST_DATE_OF_THIS_YEAR = date(day=31, month=12, year=date.today().year)
        self.LAST_DATE_OF_PREVIOUS_YEAR = date(day=31, month=12, year=date.today().year - 1)
        self.FIRST_DATE_OF_NEXT_YEAR = date(day=1, month=1, year=date.today().year + 1)
        self.HTML_MONTH_REPORT_PATH = TEST_REPORT_PATH.joinpath('year_report.html')
        self.PDF_MONTH_REPORT_PATH = TEST_REPORT_PATH.joinpath('year_report.pdf')

    def tearDown(self):
        RepositoryFactory.close_session()
        delete_all_products_from_database()

    def test_get_sales(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sales = SaleGenerator.generate_sales_from_product(product, 5)
        s1, s2, s3, s4, s5 = sales
        s1.date = self.LAST_DATE_OF_PREVIOUS_YEAR
        s2.date = self.FIRST_DATE_OF_THIS_YEAR
        s3.date = self.FIRST_DATE_OF_THIS_YEAR + timedelta(days=60)
        s4.date = self.LAST_DATE_OF_THIS_YEAR
        s5.date = self.FIRST_DATE_OF_NEXT_YEAR
        insert_sales_and_return_them(sales)

        report = YearSaleReport(self.FIRST_DATE_OF_THIS_YEAR, self.sale_repository)
        report_sales = report.get_sales()

        self.assertEqual(report_sales, [s2, s3, s4])
