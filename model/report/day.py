from datetime import date
from model.report.abstract_report import AbstractSaleReport
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
