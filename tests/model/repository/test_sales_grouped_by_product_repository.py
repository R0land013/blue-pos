from datetime import date
from unittest import TestCase

from model.report.sales_grouped_by_product import SalesGroupedByProduct
from model.repository.factory import RepositoryFactory
from model.util.monetary_types import CUPMoney
from tests.util.general import TEST_DB_URL, delete_all_products_from_database, \
    insert_products_in_database_and_return_them, insert_sales_and_return_them
from tests.util.generators.product import ProductGenerator
from tests.util.generators.sale import SaleGenerator


class TestSalesGroupedByProductRepository(TestCase):

    def setUp(self):
        self.sales_grouped_repo = RepositoryFactory.get_sales_grouped_by_product_repository(TEST_DB_URL)

    def tearDown(self):
        RepositoryFactory.close_session()
        delete_all_products_from_database()

    def test_get_groups_on_week(self):
        products = ProductGenerator.generate_products_by_quantity(2)
        p1, p2 = products
        p1.price, p1.cost = CUPMoney('3.00'), CUPMoney('2.00')  # 1.00 profit
        p2.price, p2.cost = CUPMoney('5.00'), CUPMoney('3.00')  # 2.00 profit
        insert_products_in_database_and_return_them(products)
        sales_of_p1 = SaleGenerator.generate_sales_from_product(p1, 3)
        sales_of_p2 = SaleGenerator.generate_sales_from_product(p2, 3)
        s1_p1, s2_p1, s3_p1 = sales_of_p1
        s1_p2, s2_p2, s3_p2 = sales_of_p2
        s1_p1.date = date(year=2000, month=6, day=18)  # sunday
        s2_p1.date = date(year=2000, month=6, day=19)  # monday
        s3_p1.date = date(year=2000, month=6, day=20)  # tuesday
        s1_p2.date = date(year=2000, month=6, day=24)  # saturday
        s2_p2.date = date(year=2000, month=6, day=25)  # sunday
        s3_p2.date = date(year=2000, month=6, day=26)  # monday
        sales_of_p1 = insert_sales_and_return_them(sales_of_p1)
        sales_of_p2 = insert_sales_and_return_them(sales_of_p2)

        groups = self.sales_grouped_repo.get_groups_on_week(week_date=date(year=2000, month=6, day=24))

        self.assertEqual(groups, [

            SalesGroupedByProduct(product_id=p1.id, product_name=p1.name, sale_quantity=2,
                                  acquired_money=p1.price * 2, total_cost=p1.cost * 2,
                                  total_profit=p1.profit * 2,
                                  initial_date=date(year=2000, month=6, day=19),  # monday
                                  final_date=date(year=2000, month=6, day=25)),  # sunday

            SalesGroupedByProduct(product_id=p2.id, product_name=p2.name, sale_quantity=2,
                                  acquired_money=p2.price * 2, total_cost=p2.cost * 2,
                                  total_profit=p2.profit * 2,
                                  initial_date=date(year=2000, month=6, day=19),  # monday
                                  final_date=date(year=2000, month=6, day=25))  # sunday
        ])

    def test_get_groups_on_month(self):
        products = ProductGenerator.generate_products_by_quantity(2)
        p1, p2 = products
        p1.price, p1.cost = CUPMoney('3.00'), CUPMoney('2.00')  # 1.00 profit
        p2.price, p2.cost = CUPMoney('5.00'), CUPMoney('3.00')  # 2.00 profit
        insert_products_in_database_and_return_them(products)
        sales_of_p1 = SaleGenerator.generate_sales_from_product(p1, 3)
        sales_of_p2 = SaleGenerator.generate_sales_from_product(p2, 3)
        s1_p1, s2_p1, s3_p1 = sales_of_p1
        s1_p2, s2_p2, s3_p2 = sales_of_p2
        s1_p1.date = date(year=2000, month=5, day=31)
        s2_p1.date = date(year=2000, month=6, day=1)
        s3_p1.date = date(year=2000, month=6, day=2)
        s1_p2.date = date(year=2000, month=6, day=29)
        s2_p2.date = date(year=2000, month=6, day=30)
        s3_p2.date = date(year=2000, month=7, day=1)
        sales_of_p1 = insert_sales_and_return_them(sales_of_p1)
        sales_of_p2 = insert_sales_and_return_them(sales_of_p2)

        groups = self.sales_grouped_repo.get_groups_on_month(month_date=date(year=2000, month=6, day=1))

        self.assertEqual(groups, [

            SalesGroupedByProduct(product_id=p1.id, product_name=p1.name, sale_quantity=2,
                                  acquired_money=p1.price * 2, total_cost=p1.cost * 2,
                                  total_profit=p1.profit * 2,
                                  initial_date=date(year=2000, month=6, day=1),
                                  final_date=date(year=2000, month=6, day=30)),

            SalesGroupedByProduct(product_id=p2.id, product_name=p2.name, sale_quantity=2,
                                  acquired_money=p2.price * 2, total_cost=p2.cost * 2,
                                  total_profit=p2.profit * 2,
                                  initial_date=date(year=2000, month=6, day=1),
                                  final_date=date(year=2000, month=6, day=30))
        ])