from datetime import date, timedelta
from unittest import TestCase

from model.report.month import MonthSaleReport
from model.repository.factory import RepositoryFactory
from tests.util.general import TEST_REPORT_PATH, TEST_DB_URL, insert_product_and_return_it, \
    insert_sales_and_return_them, assert_sale_lists_are_equal_ignoring_id
from tests.util.generators.product import ProductGenerator
from tests.util.generators.sale import SaleGenerator


class TestMonthSaleReport(TestCase):

    def setUp(self):
        self.sale_repository = RepositoryFactory.get_sale_repository(TEST_DB_URL)
        this_month = date.today().month
        this_year = date.today().year
        self.THIS_MONTH_DATE = date(this_year, this_month, 1)
        self.PREVIOUS_MONTH_DATE = self.THIS_MONTH_DATE - timedelta(days=1)
        self.HTML_MONTH_REPORT_PATH = TEST_REPORT_PATH.joinpath('month_report.html')
        self.PDF_MONTH_REPORT_PATH = TEST_REPORT_PATH.joinpath('month_report.pdf')

    def test_get_sales(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sales = SaleGenerator.generate_sales_from_product(product, 5)
        s1, s2, s3, s4, s5 = sales
        s1.date = self.PREVIOUS_MONTH_DATE - timedelta(days=1)
        s2.date = self.PREVIOUS_MONTH_DATE - timedelta(days=2)
        s3.date = self.THIS_MONTH_DATE + timedelta(days=1)
        s4.date = self.THIS_MONTH_DATE + timedelta(days=2)
        s5.date = self.THIS_MONTH_DATE + timedelta(days=3)
        insert_sales_and_return_them(sales)

        report = MonthSaleReport(self.THIS_MONTH_DATE, self.sale_repository)
        sales_of_report = report.get_sales()

        assert_sale_lists_are_equal_ignoring_id(sales_of_report, [s3, s4, s5])
