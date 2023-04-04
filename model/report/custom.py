from datetime import date
from typing import List
from model.report.abstract_report import AbstractSaleReport
from model.repository.expense import ExpenseRepository
from model.repository.sale import SaleRepository
from model.repository.sales_grouped_by_product import SalesGroupedByProductRepository


class CustomSaleReport(AbstractSaleReport):

    def __init__(self,
                 initial_date: date,
                 final_date: date,
                 product_id_list: List[int],
                 sale_repository: SaleRepository,
                 expense_repo: ExpenseRepository,
                 grouped_sales_repo: SalesGroupedByProductRepository,
                 name: str = None,
                 description: str = None):

        super().__init__(initial_date=initial_date,
                         final_date=final_date,
                         product_id_list=product_id_list,
                         sale_repository=sale_repository,
                         expense_repo=expense_repo,
                         grouped_sales_repo=grouped_sales_repo)

        self.__name = name
        self.__description = description

    def get_report_as_html(self) -> str:
        return self._construct_sales_grouped_report_as_html('custom_report.html',
                                                            report_name=self.__name,
                                                            description=self.__description,
                                                            initial_date=self._initial_date,
                                                            final_date=self._final_date)