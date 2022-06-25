from datetime import date, timedelta
from unittest import TestCase

from model.report.generators import generate_html_file, generate_pdf_file
from model.report.month import MonthSaleReport
from model.repository.factory import RepositoryFactory
from tests.util.general import TEST_REPORT_PATH, TEST_DB_URL, insert_product_and_return_it, \
    insert_sales_and_return_them, assert_sale_lists_are_equal_ignoring_id, delete_all_products_from_database
from tests.util.generators.product import ProductGenerator
from tests.util.generators.sale import SaleGenerator


class TestMonthSaleReport(TestCase):

    def setUp(self):
        self.sale_repository = RepositoryFactory.get_sale_repository(TEST_DB_URL)
        this_month = date.today().month
        this_year = date.today().year
        self.FIRST_DATE_OF_THIS_MONTH = date(this_year, this_month, 1)
        self.LAST_DATE_OF_THIS_MONTH = self.__get_last_date_of_this_month()
        self.LAST_DATE_OF_PREVIOUS_MONTH = self.FIRST_DATE_OF_THIS_MONTH - timedelta(days=1)
        self.HTML_MONTH_REPORT_PATH = TEST_REPORT_PATH.joinpath('month_report.html')
        self.PDF_MONTH_REPORT_PATH = TEST_REPORT_PATH.joinpath('month_report.pdf')

    def __get_last_date_of_this_month(self):
        if self.FIRST_DATE_OF_THIS_MONTH.month == 12:
            next_month = 1
        else:
            next_month = self.FIRST_DATE_OF_THIS_MONTH.month + 1
        this_year = self.FIRST_DATE_OF_THIS_MONTH.year
        first_date_next_month = date(day=1, month=next_month, year=this_year)
        return first_date_next_month - timedelta(days=1)

    def tearDown(self):
        RepositoryFactory.close_session()
        delete_all_products_from_database()

    def test_get_sales(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sales = SaleGenerator.generate_sales_from_product(product, 5)
        s1, s2, s3, s4, s5 = sales
        s1.date = self.LAST_DATE_OF_PREVIOUS_MONTH - timedelta(days=1)
        s2.date = self.LAST_DATE_OF_PREVIOUS_MONTH - timedelta(days=2)

        s3.date = self.FIRST_DATE_OF_THIS_MONTH
        s4.date = self.FIRST_DATE_OF_THIS_MONTH + timedelta(days=10)
        s5.date = self.LAST_DATE_OF_THIS_MONTH
        insert_sales_and_return_them(sales)

        report = MonthSaleReport(self.FIRST_DATE_OF_THIS_MONTH, self.sale_repository)
        sales_of_report = report.get_sales()

        self.assertEqual(sales_of_report, [s3, s4, s5])

    def test_html_report_is_generated(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sales = SaleGenerator.generate_sales_from_product(product, 3)
        s1, s2, s3 = sales
        s1.date = self.FIRST_DATE_OF_THIS_MONTH
        s2.date = self.FIRST_DATE_OF_THIS_MONTH + timedelta(days=10)
        s3.date = self.LAST_DATE_OF_THIS_MONTH
        insert_sales_and_return_them(sales)

        report = MonthSaleReport(self.FIRST_DATE_OF_THIS_MONTH, self.sale_repository)
        generate_html_file(self.HTML_MONTH_REPORT_PATH, report)

    def test_pdf_report_is_generated(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sales = SaleGenerator.generate_sales_from_product(product, 3)
        s1, s2, s3 = sales
        s1.date = self.FIRST_DATE_OF_THIS_MONTH
        s2.date = self.FIRST_DATE_OF_THIS_MONTH + timedelta(days=10)
        s3.date = self.LAST_DATE_OF_THIS_MONTH
        insert_sales_and_return_them(sales)

        report = MonthSaleReport(self.FIRST_DATE_OF_THIS_MONTH, self.sale_repository)
        generate_pdf_file(self.PDF_MONTH_REPORT_PATH, report)
