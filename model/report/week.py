from datetime import date, timedelta
from functools import reduce

from jinja2 import Template, Environment, PackageLoader, select_autoescape

from model.economy import calculate_total_profit, calculate_collected_money
from model.report.abstract_report import AbstractSaleReport
from model.repository.expense import ExpenseRepository
from model.repository.sale import SaleRepository
from model.repository.sales_grouped_by_product import SalesGroupedByProductRepository


class WeekSaleReport(AbstractSaleReport):

    def __init__(self, week_day: date, sale_repository: SaleRepository,
                 grouped_sales_repo: SalesGroupedByProductRepository,
                 expense_repo: ExpenseRepository):

        monday_date = self.__get_monday_date(week_day)
        sunday_date = self.__get_sunday_date(week_day)
        super().__init__(initial_date=monday_date,
                         final_date=sunday_date,
                         sale_repository=sale_repository,
                         grouped_sales_repo=grouped_sales_repo,
                         expense_repo=expense_repo)

    @staticmethod
    def __get_monday_date(week_day_date: date):
        if week_day_date.weekday() > 0:
            return week_day_date - timedelta(days=week_day_date.weekday())
        return week_day_date

    @staticmethod
    def __get_sunday_date(week_day_date: date):
        return week_day_date + timedelta(days=6 - week_day_date.weekday())

    def get_report_as_html(self) -> str:
        final_date = date.today() if self._final_date > date.today() else self._final_date

        report_statistics = self.get_report_statistics()
        total_collected_money = report_statistics.paid_money()
        total_cost = report_statistics.cost_money()
        total_profit = report_statistics.profit_money()
        total_expense = report_statistics.total_expenses()
        net_profit = report_statistics.net_profit()

        sales_grouped = self.get_sales_grouped_by_product()
        sale_quantity = reduce(lambda quantity, group: quantity + group.sale_quantity, sales_grouped, 0)

        template = self.get_template()
        return template.render(initial_date=self._initial_date,
                               final_date=self._final_date,
                               sale_quantity=sale_quantity,
                               total_collected_money=total_collected_money.amount,
                               total_cost=total_cost.amount,
                               total_profit=total_profit.amount,
                               total_expense=total_expense.amount,
                               net_profit=net_profit.amount,
                               sale_groups=sales_grouped)

    def get_template(self) -> Template:
        env = Environment(
            loader=PackageLoader('model.report'),
            autoescape=select_autoescape()
        )
        return env.get_template('week_report.html')
