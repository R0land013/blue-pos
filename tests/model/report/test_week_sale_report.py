import unittest
from datetime import date, timedelta

from model.report.generators import generate_html_file, generate_pdf_file
from model.report.week import WeekSaleReport
from model.repository.factory import RepositoryFactory
from tests.util.general import TEST_DB_URL, delete_all_products_from_database, \
    insert_products_in_database_and_return_them, insert_sales_and_return_them, TEST_REPORT_PATH, \
    delete_all_expenses_from_database
from tests.util.generators.product import ProductGenerator
from tests.util.generators.sale import SaleGenerator


class TestWeekSaleReport(unittest.TestCase):

    def setUp(self) -> None:
        self.sale_repository = RepositoryFactory.get_sale_repository(TEST_DB_URL)
        self.sale_groups_repo = RepositoryFactory.get_sales_grouped_by_product_repository(TEST_DB_URL)
        self.expenses_repo = RepositoryFactory.get_expense_repository(TEST_DB_URL)
        today = date.today()
        self.SUNDAY_DATE_PREVIOUS_WEEK = today - timedelta(days=today.weekday() + 1)
        self.MONDAY_DATE_THIS_WEEK = self.__get_monday_date_of_this_week()
        self.SUNDAY_DATE_THIS_WEEK = self.__get_sunday_date_of_this_week()
        self.WEDNESDAY_DATE_THIS_WEEK = self.__get_wednesday_date_of_this_week()
        self.MONDAY_DATE_NEXT_WEEK = self.__get_monday_date_next_week()

        self.HTML_WEEK_REPORT_PATH = TEST_REPORT_PATH.joinpath('week_report.html')
        self.PDF_WEEK_REPORT_PATH = TEST_REPORT_PATH.joinpath('week_report.pdf')

    @staticmethod
    def __get_monday_date_of_this_week() -> date:
        today = date.today()
        if today.weekday() > 0:
            return today - timedelta(days=today.weekday())
        return today

    @staticmethod
    def __get_sunday_date_of_this_week() -> date:
        today = date.today()
        if today.weekday() < 6:
            return today + timedelta(days=6 - today.weekday())
        return today

    @staticmethod
    def __get_wednesday_date_of_this_week() -> date:
        today = date.today()
        if today.weekday() < 2:
            return today + timedelta(days=2 - today.weekday())
        elif today.weekday() > 2:
            return today - timedelta(days=today.weekday() - 2)
        return today

    @staticmethod
    def __get_monday_date_next_week() -> date:
        today = date.today()
        return today + timedelta(days=(6 - today.weekday()) + 1)

    def tearDown(self):
        RepositoryFactory.close_session()
        delete_all_products_from_database()
        delete_all_expenses_from_database()

    def test_html_report_is_correctly_generated(self):
        products = ProductGenerator.generate_products_by_quantity(2)
        p1, p2 = insert_products_in_database_and_return_them(products)
        sales_of_p1 = SaleGenerator.generate_sales_from_product(p1, 3)
        sales_of_p2 = SaleGenerator.generate_sales_from_product(p2, 3)
        s1, s2, s3 = sales_of_p1
        s4, s5, s6 = sales_of_p2
        s1.date = self.SUNDAY_DATE_PREVIOUS_WEEK
        s2.date = self.MONDAY_DATE_THIS_WEEK
        s3.date = self.WEDNESDAY_DATE_THIS_WEEK
        s4.date = self.WEDNESDAY_DATE_THIS_WEEK
        s5.date = self.SUNDAY_DATE_THIS_WEEK
        s6.date = self.MONDAY_DATE_NEXT_WEEK
        s1, s2, s3 = insert_sales_and_return_them(sales_of_p1)
        s4, s5, s6 = insert_sales_and_return_them(sales_of_p2)

        week_report = WeekSaleReport(self.WEDNESDAY_DATE_THIS_WEEK, self.sale_repository,
                                     grouped_sales_repo=self.sale_groups_repo,
                                     expense_repo=self.expenses_repo)
        generate_html_file(self.HTML_WEEK_REPORT_PATH, week_report)

    def test_pdf_report_is_correctly_generated(self):
        products = ProductGenerator.generate_products_by_quantity(2)
        p1, p2 = insert_products_in_database_and_return_them(products)
        sales_of_p1 = SaleGenerator.generate_sales_from_product(p1, 3)
        sales_of_p2 = SaleGenerator.generate_sales_from_product(p2, 3)
        s1, s2, s3 = sales_of_p1
        s4, s5, s6 = sales_of_p2
        s1.date = self.SUNDAY_DATE_PREVIOUS_WEEK
        s2.date = self.MONDAY_DATE_THIS_WEEK
        s3.date = self.WEDNESDAY_DATE_THIS_WEEK
        s4.date = self.WEDNESDAY_DATE_THIS_WEEK
        s5.date = self.SUNDAY_DATE_THIS_WEEK
        s6.date = self.MONDAY_DATE_NEXT_WEEK
        s1, s2, s3 = insert_sales_and_return_them(sales_of_p1)
        s4, s5, s6 = insert_sales_and_return_them(sales_of_p2)

        week_report = WeekSaleReport(self.WEDNESDAY_DATE_THIS_WEEK, self.sale_repository,
                                     grouped_sales_repo=self.sale_groups_repo,
                                     expense_repo=self.expenses_repo)
        generate_pdf_file(self.PDF_WEEK_REPORT_PATH, week_report)
