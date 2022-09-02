from datetime import date
from functools import reduce
from typing import List
from model.entity.models import Expense, Sale
from model.report.sales_grouped_by_product import SalesGroupedByProduct
from model.report.statistics import ReportStatistic
from model.repository.expense import ExpenseRepository, ExpenseFilter
from model.repository.sale import SaleRepository, SaleFilter
from model.repository.sales_grouped_by_product import SalesGroupedByProductRepository
from model.util.monetary_types import CUPMoney


class AbstractSaleReport:
    """
    Representa un reporte que se calcula entre dos fechas límites.
    """

    def __init__(self, initial_date: date,
                 final_date: date,
                 sale_repository: SaleRepository,
                 grouped_sales_repo: SalesGroupedByProductRepository,
                 expense_repo: ExpenseRepository,
                 product_id_list: List[int] = None):

        self._initial_date = initial_date
        self._final_date = final_date
        self._sale_repo = sale_repository
        self._grouped_sales_repo = grouped_sales_repo
        self._expense_repo = expense_repo
        self._product_id_list = product_id_list

    def get_sales(self) -> List[Sale]:
        sale_filter = SaleFilter()
        sale_filter.minimum_date = self._initial_date
        sale_filter.maximum_date = self._final_date
        return self._sale_repo.get_sales_by_filter(sale_filter)

    def get_sales_grouped_by_product(self) -> List[SalesGroupedByProduct]:
        return self._grouped_sales_repo.get_groups_on_date_range(self._initial_date, self._final_date,
                                                                 product_id_list=self._product_id_list)

    def get_expenses(self) -> List[Expense]:
        expense_filter = ExpenseFilter()
        expense_filter.minimum_date = self._initial_date
        expense_filter.maximum_date = self._final_date
        return self._expense_repo.get_expenses_by_filter(expense_filter)

    def get_report_as_html(self) -> str:
        raise NotImplementedError()

    def get_report_statistics(self) -> ReportStatistic:
        sales_grouped = self.get_sales_grouped_by_product()

        sale_quantity = reduce(lambda quantity, group: quantity + group.sale_quantity, sales_grouped, 0)
        collected_money = reduce(lambda collected, group: collected + group.acquired_money,
                                 sales_grouped, CUPMoney('0'))
        cost_money = reduce(lambda cost, group: cost + group.total_cost, sales_grouped, CUPMoney('0'))

        expense_list = self.get_expenses()
        total_expense = reduce(lambda expense_money, expense: expense_money + expense.spent_money,
                               expense_list, CUPMoney('0'))

        return ReportStatistic(sale_quantity=sale_quantity, paid_money=collected_money,
                               cost_money=cost_money, total_expenses=total_expense,
                               initial_date=self._initial_date,
                               final_date=self._final_date)
