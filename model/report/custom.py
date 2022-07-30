from model.report.abstract_report import AbstractSaleReport
from model.report.statistics import ReportStatistic
from model.repository.sale import SaleFilter, SaleRepository


class CustomSaleReport(AbstractSaleReport):

    def __init__(self, sale_filter: SaleFilter, sale_repository: SaleRepository):
        self.__custom_sale_filter = sale_filter
        self.__sale_repo = sale_repository

    def get_sales(self) -> list:
        return self.__sale_repo.get_sales_by_filter(self.__custom_sale_filter)

    def get_report_as_html(self) -> str:
        pass

    def get_report_statistics(self) -> ReportStatistic:
        pass
