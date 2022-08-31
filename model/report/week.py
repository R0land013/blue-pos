from datetime import date, timedelta
from functools import reduce
from typing import List

from jinja2 import Template, Environment, PackageLoader, select_autoescape

from model.economy import calculate_total_profit, calculate_collected_money
from model.entity.models import Expense
from model.report.abstract_report import AbstractSaleReport
from model.report.sales_grouped_by_product import SalesGroupedByProduct
from model.report.statistics import ReportStatistic
from model.repository.expense import ExpenseRepository, ExpenseFilter
from model.repository.sale import SaleRepository, SaleFilter
from model.repository.sales_grouped_by_product import SalesGroupedByProductRepository
from model.util.monetary_types import CUPMoney


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
        sales = self.get_sales()
        total_profit = calculate_total_profit(sales)
        total_collected_money = calculate_collected_money(sales)

        template = self.get_template()
        return template.render(monday_date=self._initial_date,
                               sunday_date=self._final_date,
                               sale_quantity=len(sales),
                               sales=sales,
                               total_profit=total_profit,
                               total_collected_money=total_collected_money)

    def get_template(self) -> Template:
        env = Environment(
            loader=PackageLoader('model.report'),
            autoescape=select_autoescape()
        )
        return env.get_template('week_report.html')
