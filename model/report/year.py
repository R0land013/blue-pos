from datetime import date

from jinja2 import Environment, PackageLoader, select_autoescape
from jinja2.nodes import Template

from model.economy import calculate_total_profit, calculate_collected_money
from model.report.abstract_report import AbstractSaleReport
from model.repository.sale import SaleRepository, SaleFilter


class YearSaleReport(AbstractSaleReport):

    def __init__(self, year_date: date, sale_repo: SaleRepository):
        self.__sale_repo = sale_repo
        self.__year_date = year_date

    def get_sales(self) -> list:
        first_date_of_year = date(day=1, month=1, year=self.__year_date.year)
        last_date_of_year = date(day=31, month=12, year=self.__year_date.year)

        sale_filter = SaleFilter()
        sale_filter.minimum_date = first_date_of_year
        sale_filter.maximum_date = last_date_of_year

        return self.__sale_repo.get_sales_by_filter(sale_filter)

    def get_report_as_html(self) -> str:
        sales = self.get_sales()
        total_profit = calculate_total_profit(sales)
        total_collected_money = calculate_collected_money(sales)

        template = self.get_template()
        return template.render(date=self.__year_date,
                               sales=sales,
                               total_profit=total_profit,
                               total_collected_money=total_collected_money)

    def get_template(self) -> Template:
        env = Environment(
            loader=PackageLoader('model.report'),
            autoescape=select_autoescape()
        )
        return env.get_template('year_report.html')
