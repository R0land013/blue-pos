from datetime import date
from model.report.abstract_report import AbstractSaleReport
from model.repository.sale import SaleRepository


class MonthSaleReport(AbstractSaleReport):

    def __init__(self, month_date: date, sale_repository: SaleRepository):
        pass

    def get_report_as_html(self) -> str:
        pass

    def get_sales(self) -> list:
        pass
