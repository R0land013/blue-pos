from datetime import date
from pathlib import Path

from model.report.abstract_report import AbstractSaleReport
from model.report.generators import generate_html_file
from model.report.template_fulfillment import fulfill_day_report_html_template
from model.repository.sale import SaleRepository, SaleFilter


class DaySaleReport(AbstractSaleReport):

    def __init__(self, day_date: date, repository: SaleRepository):
        self.__day_date = day_date
        self.__sale_repository = repository

    def get_sales(self) -> list:
        sale_filter = SaleFilter()
        sale_filter.minimum_date = self.__day_date
        sale_filter.maximum_date = self.__day_date

        return self.__sale_repository.get_sales_by_filter(sale_filter)

    def generate_report_as_html(self, path: Path):
        fulfilled_template = fulfill_day_report_html_template(self.get_sales())
        generate_html_file(path, fulfilled_template)
