import unittest
from datetime import date, timedelta

from model.report.custom import CustomSaleReport
from model.report.generators import generate_html_file
from model.repository.factory import RepositoryFactory
from model.repository.sale import SaleFilter
from model.util.monetary_types import CUPMoney
from tests.util.general import TEST_REPORT_PATH, TEST_DB_URL, delete_all_products_from_database, \
    insert_products_in_database_and_return_them, insert_sales_and_return_them
from tests.util.generators.product import ProductGenerator
from tests.util.generators.sale import SaleGenerator


class TestCustomSaleReport(unittest.TestCase):

    def setUp(self) -> None:
        self.sale_repository = RepositoryFactory.get_sale_repository(TEST_DB_URL)
        self.TODAY_DATE = date.today()
        self.YESTERDAY_DATE = date.today() - timedelta(days=1)
        self.HTML_CUSTOM_REPORT_PATH = TEST_REPORT_PATH.joinpath('custom_report.html')

    def tearDown(self):
        RepositoryFactory.close_session()
        delete_all_products_from_database()

    def test_html_report_is_correctly_generated(self):
        p1, p2 = ProductGenerator.generate_products_by_quantity(2)
        p1, p2 = insert_products_in_database_and_return_them([p1, p2])
        sales_of_p1 = SaleGenerator.generate_sales_from_product(p1, 3)
        sales_of_p2 = SaleGenerator.generate_sales_from_product(p2, 3)
        s1, s2, s3 = sales_of_p1
        s4, s5, s6 = sales_of_p2
        s1.date = self.TODAY_DATE
        s2.date = self.YESTERDAY_DATE
        s3.date = self.TODAY_DATE
        s4.date = self.YESTERDAY_DATE
        s5.date = self.TODAY_DATE
        s6.date = self.YESTERDAY_DATE
        s1, s2, s3 = insert_sales_and_return_them(sales_of_p1)
        s4, s5, s6 = insert_sales_and_return_them(sales_of_p2)

        custom_filter = SaleFilter()
        custom_filter.product_id_list = [p1.id]
        custom_filter.minimum_date = self.TODAY_DATE
        report_name = 'Ventas de Juan'
        description = 'Los productos que se vendieron hoy y que eran propiedad de juanito.'
        custom_report = CustomSaleReport(custom_filter, self.sale_repository, report_name, description)

        generate_html_file(self.HTML_CUSTOM_REPORT_PATH, custom_report)
