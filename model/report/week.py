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
        self.__week_day_date = week_day
        self.__sale_repository = sale_repository
        self.__grouped_sales_repo = grouped_sales_repo
        self.__expense_repo = expense_repo

    def get_sales(self) -> list:
        week_filter = SaleFilter()
        week_filter.minimum_date = self.__get_monday_date()
        week_filter.maximum_date = self.__get_sunday_date()

        return self.__sale_repository.get_sales_by_filter(week_filter)

    def __get_monday_date(self):
        if self.__week_day_date.weekday() > 0:
            return self.__week_day_date - timedelta(days=self.__week_day_date.weekday())
        return self.__week_day_date

    def __get_sunday_date(self):
        return self.__week_day_date + timedelta(days=6 - self.__week_day_date.weekday())

    def get_report_as_html(self) -> str:
        sales = self.get_sales()
        total_profit = calculate_total_profit(sales)
        total_collected_money = calculate_collected_money(sales)

        template = self.get_template()
        return template.render(monday_date=self.__get_monday_date(),
                               sunday_date=self.__get_sunday_date(),
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

    def get_report_statistics(self) -> ReportStatistic:
        sales_grouped = self.get_sales_grouped_by_product()

        sale_quantity = reduce(lambda quantity, group: quantity + group.sale_quantity, sales_grouped, 0)
        collected_money = reduce(lambda collected, group: collected + group.acquired_money,
                                 sales_grouped, CUPMoney('0'))
        cost_money = reduce(lambda cost, group: cost + group.total_cost, sales_grouped, CUPMoney('0'))

        expense_list = self.get_expenses()
        total_expense = reduce(lambda expense_money, expense: expense_money + expense.spent_money,
                               expense_list, CUPMoney('0'))

        return ReportStatistic(sale_quantity=sale_quantity, paid_money=collected_money,
                               cost_money=cost_money, total_expenses=total_expense,
                               initial_date=self.__get_monday_date(),
                               final_date=self.__get_sunday_date())

    def get_expenses(self) -> List[Expense]:
        week_expense_filter = ExpenseFilter()
        week_expense_filter.minimum_date = self.__get_monday_date()
        week_expense_filter.maximum_date = self.__get_sunday_date()
        return self.__expense_repo.get_expenses_by_filter(week_expense_filter)

    def get_sales_grouped_by_product(self) -> List[SalesGroupedByProduct]:
        return self.__grouped_sales_repo.get_groups_on_week(self.__week_day_date)
