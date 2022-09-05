from datetime import date
from unittest import TestCase

from model.entity.economic_summary import EconomicSummary
from model.repository.factory import RepositoryFactory
from model.util.monetary_types import CUPMoney
from tests.util.general import TEST_DB_URL, delete_all_products_from_database, delete_all_expenses_from_database, \
    insert_products_in_database_and_return_them, insert_sales_and_return_them, insert_expenses_in_database
from tests.util.generators.expense import ExpenseGenerator
from tests.util.generators.product import ProductGenerator
from tests.util.generators.sale import SaleGenerator


class TestEconomicSummaryRepository(TestCase):

    def setUp(self):
        self.economic_summary_repo = RepositoryFactory.get_economic_summary_repository(TEST_DB_URL)

    def tearDown(self):
        RepositoryFactory.close_session()
        delete_all_products_from_database()
        delete_all_expenses_from_database()

    def test_get_economic_summary_on_month(self):
        products = ProductGenerator.generate_products_by_quantity(2)
        p1, p2 = products
        p1.price, p1.cost = CUPMoney('3.00'), CUPMoney('2.00')  # 1.00 profit
        p2.price, p2.cost = CUPMoney('5.00'), CUPMoney('3.00')  # 2.00 profit
        insert_products_in_database_and_return_them(products)
        sales_of_p1 = SaleGenerator.generate_sales_from_product(p1, 3)
        sales_of_p2 = SaleGenerator.generate_sales_from_product(p2, 3)
        s1, s2, s3 = sales_of_p1
        s4, s5, s6 = sales_of_p2
        s1.date = date(year=2000, month=11, day=30)
        s2.date = date(year=2000, month=12, day=1)
        s3.date = date(year=2000, month=12, day=2)
        s4.date = date(year=2000, month=12, day=30)
        s5.date = date(year=2000, month=12, day=31)
        s6.date = date(year=2000, month=11, day=1)
        insert_sales_and_return_them(sales_of_p1)
        insert_sales_and_return_them(sales_of_p2)
        expenses = ExpenseGenerator.generate_expenses_by_quantity(3)
        e1, e2, e3 = expenses
        e1.date, e1.spent_money = date(year=2000, month=11, day=30), CUPMoney('2.00')
        e2.date, e2.spent_money = date(year=2000, month=12, day=1), CUPMoney('1.00')
        e3.date, e3.spent_money = date(year=2000, month=12, day=31), CUPMoney('2.00')
        insert_expenses_in_database(expenses)

        december_summary = self.economic_summary_repo.get_economic_summary_on_month(
            date(year=2000, month=12, day=1)
        )

        self.assertEqual(december_summary, EconomicSummary(
            initial_date=date(day=1, month=12, year=2000),
            final_date=date(day=31, month=12, year=2000),
            sale_quantity=4,  # s2, s3, s4, s5
            acquired_money=CUPMoney('16.00'),
            total_cost=CUPMoney('10.00'),
            total_profit=CUPMoney('6.00'),
            total_expense=CUPMoney('3.00'),
            net_profit=CUPMoney('3.00')
        ))
