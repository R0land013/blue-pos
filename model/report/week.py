from datetime import date

from model.report.abstract_report import AbstractSaleReport
from model.report.statistics import ReportStatistic
from model.repository.sale import SaleRepository


class WeekSaleReport(AbstractSaleReport):

    def __init__(self, week_day: date, sale_repository: SaleRepository):
        pass

    def get_sales(self) -> list:
        pass

    def get_report_as_html(self) -> str:
        pass

    def get_report_statistics(self) -> ReportStatistic:
        pass
