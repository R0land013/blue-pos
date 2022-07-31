from jinja2 import Template, Environment, PackageLoader, select_autoescape

from model.economy import calculate_total_profit, calculate_collected_money
from model.report.abstract_report import AbstractSaleReport
from model.report.statistics import ReportStatistic
from model.repository.sale import SaleFilter, SaleRepository


class CustomSaleReport(AbstractSaleReport):

    def __init__(self, sale_filter: SaleFilter, sale_repository: SaleRepository,
                 name: str = None, description: str = None):
        self.__custom_sale_filter = sale_filter
        self.__sale_repo = sale_repository
        self.__name = name
        self.__description = description

    def get_sales(self) -> list:
        return self.__sale_repo.get_sales_by_filter(self.__custom_sale_filter)

    def get_report_as_html(self) -> str:
        sales = self.get_sales()
        total_profit = calculate_total_profit(sales)
        total_collected_money = calculate_collected_money(sales)

        template = self.get_template()
        return template.render(report_name=self.__name,
                               initial_date=self.__custom_sale_filter.minimum_date,
                               final_date=self.__custom_sale_filter.maximum_date,
                               description=self.__description,
                               sales=sales,
                               sale_quantity=len(sales),
                               total_profit=total_profit,
                               total_collected_money=total_collected_money)

    def get_template(self) -> Template:
        env = Environment(
            loader=PackageLoader('model.report'),
            autoescape=select_autoescape()
        )
        return env.get_template('custom_report.html')

    def get_report_statistics(self) -> ReportStatistic:
        pass
