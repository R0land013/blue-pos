from datetime import date
from unittest import TestCase

from model.report.abstract_report import AbstractSaleReport
from model.repository.factory import RepositoryFactory
from tests.util.general import insert_products_in_database_and_return_them, insert_sales_and_return_them, TEST_DB_URL, \
    delete_all_products_from_database, delete_all_expenses_from_database
from tests.util.generators.product import ProductGenerator
from tests.util.generators.sale import SaleGenerator


class TestAbstractSaleReport(TestCase):

    def setUp(self):
        self.sale_repo = RepositoryFactory.get_sale_repository(TEST_DB_URL)
        self.expense_repo = RepositoryFactory.get_expense_repository(TEST_DB_URL)
        self.sale_group_repo = RepositoryFactory.get_sales_grouped_by_product_repository(TEST_DB_URL)

    def tearDown(self):
        RepositoryFactory.close_session()
        delete_all_products_from_database()
        delete_all_expenses_from_database()

    def test_get_sales(self):
        products = ProductGenerator.generate_products_by_quantity(2)
        p1, p2 = products
        insert_products_in_database_and_return_them(products)
        sales_of_p1 = SaleGenerator.generate_sales_from_product(p1, 3)
        sales_of_p2 = SaleGenerator.generate_sales_from_product(p2, 3)
        s1, s2, s3 = sales_of_p1
        s4, s5, s6 = sales_of_p2
        s1.date = date(year=2000, month=6, day=20)
        s2.date = date(year=2000, month=6, day=21)
        s3.date = date(year=2000, month=6, day=22)
        s4.date = date(year=2000, month=6, day=23)
        s5.date = date(year=2000, month=6, day=24)
        s6.date = date(year=2000, month=6, day=25)
        insert_sales_and_return_them(sales_of_p1)
        insert_sales_and_return_them(sales_of_p2)

        report = AbstractSaleReport(initial_date=date(year=2000, month=6, day=21),
                                    final_date=date(year=2000, month=6, day=24),
                                    sale_repository=self.sale_repo,
                                    expense_repo=self.expense_repo,
                                    grouped_sales_repo=self.sale_group_repo)
        sales_from_report = report.get_sales()

        self.assertEqual(sales_from_report, [s2, s3, s4, s5])
