from datetime import date, timedelta

from model.report.abstract_report import AbstractSaleReport
from model.report.statistics import ReportStatistic
from model.repository.sale import SaleRepository, SaleFilter


class WeekSaleReport(AbstractSaleReport):

    def __init__(self, week_day: date, sale_repository: SaleRepository):
        self.__week_day_date = week_day
        self.__sale_repository = sale_repository

    def get_sales(self) -> list:
        week_filter = SaleFilter()
        week_filter.minimum_date = self.__get_monday_date()
        week_filter.maximum_date = self.get_sunday_date()

        return self.__sale_repository.get_sales_by_filter(week_filter)

    def __get_monday_date(self):
        if self.__week_day_date.weekday() > 0:
            return self.__week_day_date - timedelta(days=self.__week_day_date.weekday())
        return self.__week_day_date

    def get_sunday_date(self):
        if self.__week_day_date.weekday() < 6:
            return self.__week_day_date + timedelta(days=6 - self.__week_day_date.weekday())

    def get_report_as_html(self) -> str:
        pass

    def get_report_statistics(self) -> ReportStatistic:
        pass
