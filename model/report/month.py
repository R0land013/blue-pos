from datetime import date, timedelta
from model.report.abstract_report import AbstractSaleReport
from model.repository.sale import SaleRepository, SaleFilter


class MonthSaleReport(AbstractSaleReport):

    def __init__(self, month_date: date, sale_repository: SaleRepository):
        self.__month_date = month_date
        self.__sale_repo = sale_repository

    def get_report_as_html(self) -> str:
        pass

    def get_sales(self) -> list:
        first_date_of_month = date(day=1,
                                   month=self.__month_date.month,
                                   year=self.__month_date.year)
        last_date_of_month = self.__get_last_date_of_month()
        a_filter = SaleFilter()
        a_filter.minimum_date = first_date_of_month
        a_filter.maximum_date = last_date_of_month
        return self.__sale_repo.get_sales_by_filter(a_filter)

    def __get_last_date_of_month(self):
        if self.__month_date.month == 12:
            month = 1
        else:
            month = self.__month_date.month + 1
        first_date_next_month = date(day=1, month=month, year=self.__month_date.year)
        return first_date_next_month - timedelta(1)
