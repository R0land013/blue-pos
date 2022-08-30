from typing import List
from model.entity.models import Expense
from model.report.sales_grouped_by_product import SalesGroupedByProduct
from model.report.statistics import ReportStatistic


class AbstractSaleReport:

    def get_sales(self) -> list:
        raise NotImplementedError()

    def get_sales_grouped_by_product(self) -> List[SalesGroupedByProduct]:
        raise NotImplementedError()

    def get_expenses(self) -> List[Expense]:
        raise NotImplementedError()

    def get_report_as_html(self) -> str:
        raise NotImplementedError()

    def get_report_statistics(self) -> ReportStatistic:
        raise NotImplementedError()
