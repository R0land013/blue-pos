import unittest
from datetime import date, timedelta
from model.report.day import DaySaleReport
from model.report.generators import generate_html_file, generate_pdf_file
from model.repository.factory import RepositoryFactory
from tests.util.general import TEST_DB_URL, delete_all_products_from_database, insert_product_and_return_it, \
    insert_sales_and_return_them, assert_sale_lists_are_equal_ignoring_id, insert_products_in_database_and_return_them, \
    TEST_REPORT_PATH
from tests.util.generators.product import ProductGenerator
from tests.util.generators.sale import SaleGenerator


class TestDaySaleReport(unittest.TestCase):

    def setUp(self) -> None:
        self.sale_repository = RepositoryFactory.get_sale_repository(TEST_DB_URL)
        self.expense_repo = RepositoryFactory.get_expense_repository(TEST_DB_URL)
        self.grouped_sales_repo = RepositoryFactory.get_sales_grouped_by_product_repository(TEST_DB_URL)
        self.TODAY = date.today()
        self.YESTERDAY = self.TODAY - timedelta(days=1)
        self.HTML_DAY_REPORT_PATH = TEST_REPORT_PATH.joinpath('day_report.html')
        self.PDF_DAY_REPORT_PATH = TEST_REPORT_PATH.joinpath('day_report.pdf')

    def tearDown(self):
        RepositoryFactory.close_session()
        delete_all_products_from_database()

    def test_html_report_is_correctly_generated(self):
        products = ProductGenerator.generate_products_by_quantity(2)
        products = insert_products_in_database_and_return_them(products)
        p1, p2 = products
        p1_sales = SaleGenerator.generate_sales_from_product(p1, 3)
        p2_sales = SaleGenerator.generate_sales_from_product(p2, 3)
        for a_sale in p1_sales:
            a_sale.date = self.TODAY
        for a_sale in p2_sales:
            a_sale.date = self.TODAY
        p1_sales = insert_sales_and_return_them(p1_sales)
        p2_sales = insert_sales_and_return_them(p2_sales)

        report = DaySaleReport(self.TODAY,
                               sale_repo=self.sale_repository,
                               expense_repo=self.expense_repo,
                               grouped_sales_repo=self.grouped_sales_repo)
        generate_html_file(self.HTML_DAY_REPORT_PATH, report)

    def test_pdf_report_is_correctly_generated(self):
        products = ProductGenerator.generate_products_by_quantity(2)
        products = insert_products_in_database_and_return_them(products)
        p1, p2 = products
        p1_sales = SaleGenerator.generate_sales_from_product(p1, 3)
        p2_sales = SaleGenerator.generate_sales_from_product(p2, 3)
        for a_sale in p1_sales:
            a_sale.date = self.TODAY
        for a_sale in p2_sales:
            a_sale.date = self.TODAY
        p1_sales = insert_sales_and_return_them(p1_sales)
        p2_sales = insert_sales_and_return_them(p2_sales)

        report = DaySaleReport(self.TODAY,
                               sale_repo=self.sale_repository,
                               expense_repo=self.expense_repo,
                               grouped_sales_repo=self.grouped_sales_repo)
        generate_pdf_file(self.PDF_DAY_REPORT_PATH, report)
