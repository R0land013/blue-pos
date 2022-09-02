from datetime import date
from typing import List
from jinja2 import Template, Environment, PackageLoader, select_autoescape
from model.economy import calculate_total_profit, calculate_collected_money
from model.report.abstract_report import AbstractSaleReport
from model.repository.expense import ExpenseRepository
from model.repository.sale import SaleFilter, SaleRepository
from model.repository.sales_grouped_by_product import SalesGroupedByProductRepository


class CustomSaleReport(AbstractSaleReport):

    def __init__(self,
                 initial_date: date,
                 final_date: date,
                 product_id_list: List[int],
                 sale_repository: SaleRepository,
                 expense_repo: ExpenseRepository,
                 grouped_sales_repo: SalesGroupedByProductRepository,
                 name: str = None,
                 description: str = None):

        super().__init__(initial_date=initial_date,
                         final_date=final_date,
                         product_id_list=product_id_list,
                         sale_repository=sale_repository,
                         expense_repo=expense_repo,
                         grouped_sales_repo=grouped_sales_repo)

        self.__name = name
        self.__description = description

    def get_sales(self) -> list:
        custom_sale_filter = SaleFilter()
        custom_sale_filter.minimum_date = self._initial_date
        custom_sale_filter.maximum_date = self._final_date
        custom_sale_filter.product_id_list = self._product_id_list
        return self._sale_repo.get_sales_by_filter(custom_sale_filter)

    def get_report_as_html(self) -> str:
        sales = self.get_sales()
        total_profit = calculate_total_profit(sales)
        total_collected_money = calculate_collected_money(sales)

        template = self.get_template()
        return template.render(report_name=self.__name,
                               initial_date=self._initial_date,
                               final_date=self._final_date,
                               description=self.__description,
                               sales=sales,
                               sale_quantity=len(sales),
                               total_profit=total_profit,
                               total_collected_money=total_collected_money)

    def get_template(self) -> Template:
        env = Environment(
            loader=PackageLoader('model.report'),
            autoescape=select_autoescape()
        )
        return env.get_template('custom_report.html')
