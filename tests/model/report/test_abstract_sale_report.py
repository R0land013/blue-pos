from datetime import date
from unittest import TestCase

from model.report.abstract_report import AbstractSaleReport
from model.report.statistics import ReportStatistic
from model.repository.factory import RepositoryFactory
from model.util.monetary_types import CUPMoney
from tests.util.general import insert_products_in_database_and_return_them, insert_sales_and_return_them, TEST_DB_URL, \
    delete_all_products_from_database, delete_all_expenses_from_database, insert_expenses_in_database
from tests.util.generators.expense import ExpenseGenerator
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

    def test_get_report_statistic(self):
        products = ProductGenerator.generate_products_by_quantity(2)
        p1, p2 = products
        p1.price, p1.cost = CUPMoney('10.00'), CUPMoney('5.00')  # profit 5.00
        p2.price, p2.cost = CUPMoney('20.00'), CUPMoney('10.00')  # profit 10.00
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
        expenses = ExpenseGenerator.generate_expenses_by_quantity(3)
        e1, e2, e3 = expenses
        e1.spent_money, e2.spent_money, e3.spent_money = CUPMoney('2.00'), CUPMoney('3.00'), CUPMoney('5.00')
        e1.date = date(year=2000, month=6, day=21)
        e2.date = date(year=2000, month=6, day=24)
        e3.date = date(year=2000, month=6, day=25)
        insert_expenses_in_database(expenses)

        week_report = AbstractSaleReport(
            initial_date=date(year=2000, month=6, day=21),
            final_date=date(year=2000, month=6, day=24),
            sale_repository=self.sale_repo,
            grouped_sales_repo=self.sale_group_repo,
            expense_repo=self.expense_repo
        )
        report_statistic = week_report.get_report_statistics()

        self.assertEqual(report_statistic,
                         ReportStatistic(
                             sale_quantity=4,  # s2, s3, s4, s5
                             paid_money=CUPMoney('60.00'),
                             cost_money=CUPMoney('30.00'),
                             total_expenses=CUPMoney('5.00'),  # e1, e2
                             initial_date=date(year=2000, month=6, day=21),
                             final_date=date(year=2000, month=6, day=24)
                         ))
