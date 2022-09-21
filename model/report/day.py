from datetime import date
from functools import reduce

from model.economy import calculate_total_profit, calculate_collected_money
from model.report.abstract_report import AbstractSaleReport
from model.repository.expense import ExpenseRepository
from model.repository.sale import SaleRepository
from jinja2 import Environment, PackageLoader, select_autoescape, Template
from model.repository.sales_grouped_by_product import SalesGroupedByProductRepository
from model.util.monetary_types import CUPMoney


class DaySaleReport(AbstractSaleReport):

    def __init__(self, day_date: date,
                 sale_repo: SaleRepository,
                 expense_repo: ExpenseRepository,
                 grouped_sales_repo: SalesGroupedByProductRepository):
        super().__init__(initial_date=day_date,
                         final_date=day_date,
                         sale_repository=sale_repo,
                         expense_repo=expense_repo,
                         grouped_sales_repo=grouped_sales_repo)

    def get_report_as_html(self) -> str:
        sales = self.get_sales()
        report_statistics = self.get_report_statistics()

        total_collected_money = report_statistics.paid_money()
        total_cost = report_statistics.cost_money()
        total_profit = report_statistics.profit_money()
        total_expense = report_statistics.total_expenses()
        net_profit = report_statistics.net_profit()

        template = self.get_template()
        return template.render(date=self._initial_date,
                               sale_quantity=len(sales),
                               total_collected_money=total_collected_money.amount,
                               total_cost=total_cost.amount,
                               total_profit=total_profit.amount,
                               total_expense=total_expense.amount,
                               net_profit=net_profit.amount,
                               sales=sales)

    def get_template(self) -> Template:
        env = Environment(
            loader=PackageLoader('model.report'),
            autoescape=select_autoescape()
        )
        return env.get_template('day_report.html')
