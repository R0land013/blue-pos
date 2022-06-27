from datetime import date

from model.report.abstract_report import AbstractSaleReport
from model.repository.sale import SaleRepository


class YearSaleReport(AbstractSaleReport):

    def __init__(self, year_date: date, sale_repo: SaleRepository):
        self.__sale_repo = sale_repo
        self.__year_date = year_date

    def get_sales(self) -> list:
        pass

    def get_report_as_html(self) -> str:
        pass
