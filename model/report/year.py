from datetime import date

from jinja2 import Environment, PackageLoader, select_autoescape
from jinja2.nodes import Template

from model.economy import calculate_total_profit, calculate_collected_money
from model.report.abstract_report import AbstractSaleReport
from model.report.statistics import ReportStatistic
from model.repository.expense import ExpenseRepository
from model.repository.sale import SaleRepository, SaleFilter
from model.repository.sales_grouped_by_product import SalesGroupedByProductRepository


class YearSaleReport(AbstractSaleReport):

    def __init__(self,
                 year_date: date,
                 sale_repo: SaleRepository,
                 sale_group_repo: SalesGroupedByProductRepository,
                 expense_repo: ExpenseRepository):

        first_date_of_year = date(year=year_date.year, month=1, day=1)
        last_date_of_year = date(year=year_date.year, month=12, day=31)
        super().__init__(initial_date=first_date_of_year,
                         final_date=last_date_of_year,
                         sale_repository=sale_repo,
                         grouped_sales_repo=sale_group_repo,
                         expense_repo=expense_repo)

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
        return env.get_template('year_report.html')
