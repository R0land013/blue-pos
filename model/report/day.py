from datetime import date
from model.economy import calculate_total_profit, calculate_collected_money
from model.report.abstract_report import AbstractSaleReport
from model.repository.sale import SaleRepository, SaleFilter
from jinja2 import Environment, PackageLoader, select_autoescape, Template


class DaySaleReport(AbstractSaleReport):

    def __init__(self, day_date: date, repository: SaleRepository):
        self.__day_date = day_date
        self.__sale_repository = repository

    def get_sales(self) -> list:
        sale_filter = SaleFilter()
        sale_filter.minimum_date = self.__day_date
        sale_filter.maximum_date = self.__day_date

        return self.__sale_repository.get_sales_by_filter(sale_filter)

    def get_report_as_html(self) -> str:
        sales = self.get_sales()
        total_profit = calculate_total_profit(sales)
        total_collected_money = calculate_collected_money(sales)

        template = self.get_template()
        return template.render(date=self.__day_date,
                               sales=sales,
                               total_profit=total_profit,
                               total_collected_money=total_collected_money)

    def get_template(self) -> Template:
        env = Environment(
            loader=PackageLoader('model.report'),
            autoescape=select_autoescape()
        )
        return env.get_template('day_report.html')

