from datetime import date, timedelta

from jinja2 import Template, Environment, PackageLoader, select_autoescape

from model.economy import calculate_total_profit, calculate_collected_money
from model.report.abstract_report import AbstractSaleReport
from model.report.statistics import ReportStatistic
from model.repository.sale import SaleRepository, SaleFilter


class WeekSaleReport(AbstractSaleReport):

    def __init__(self, week_day: date, sale_repository: SaleRepository):
        self.__week_day_date = week_day
        self.__sale_repository = sale_repository

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
        if self.__week_day_date.weekday() < 6:
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
        sales = self.get_sales()
        profit_money = calculate_total_profit(sales)
        collected_money = calculate_collected_money(sales)

        return ReportStatistic(sale_quantity=len(sales), paid_money=collected_money,
                               profit_money=profit_money, initial_date=self.__get_monday_date(),
                               final_date=self.__get_sunday_date())
