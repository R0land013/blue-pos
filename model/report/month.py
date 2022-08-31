from datetime import date, timedelta
from jinja2 import Environment, PackageLoader, select_autoescape
from jinja2.nodes import Template
from model.economy import calculate_total_profit, calculate_collected_money
from model.report.abstract_report import AbstractSaleReport
from model.repository.expense import ExpenseRepository
from model.repository.sale import SaleRepository
from model.repository.sales_grouped_by_product import SalesGroupedByProductRepository


class MonthSaleReport(AbstractSaleReport):

    def __init__(self, month_date: date,
                 sale_repository: SaleRepository,
                 expense_repo: ExpenseRepository,
                 grouped_sales_repo: SalesGroupedByProductRepository):

        first_date_of_month = date(year=month_date.year, month=month_date.month, day=1)
        last_date_of_month = self.__get_last_date_of_month(month_date)
        super().__init__(
            initial_date=first_date_of_month,
            final_date=last_date_of_month,
            sale_repository=sale_repository,
            expense_repo=expense_repo,
            grouped_sales_repo=grouped_sales_repo
        )

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
        return env.get_template('month_report.html')

    @staticmethod
    def __get_last_date_of_month(month_date: date):
        if month_date.month == 12:
            next_month = 1
        else:
            next_month = month_date.month + 1

        if next_month == 1:
            first_date_next_month = date(day=1, month=1, year=month_date.year + 1)
        else:
            first_date_next_month = date(day=1, month=next_month, year=month_date.year)

        return first_date_next_month - timedelta(days=1)
