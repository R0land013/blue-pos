from datetime import date
from model.economy import calculate_total_profit, calculate_collected_money
from model.report.abstract_report import AbstractSaleReport
from model.repository.expense import ExpenseRepository
from model.repository.sale import SaleRepository
from jinja2 import Environment, PackageLoader, select_autoescape, Template
from model.repository.sales_grouped_by_product import SalesGroupedByProductRepository


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
        total_profit = calculate_total_profit(sales)
        total_collected_money = calculate_collected_money(sales)

        template = self.get_template()
        return template.render(date=self._initial_date,
                               sale_quantity=len(sales),
                               sales=sales,
                               total_profit=total_profit,
                               total_collected_money=total_collected_money)

    def get_template(self) -> Template:
        env = Environment(
            loader=PackageLoader('model.report'),
            autoescape=select_autoescape()
        )
        return env.get_template('day_report.html')
