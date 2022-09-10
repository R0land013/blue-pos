from datetime import date, timedelta
from sqlalchemy.orm import Session
from model.entity.economic_summary import EconomicSummary
from sqlalchemy import func, cast, FLOAT, select

from model.entity.models import Sale, Expense
from model.util.monetary_types import CUPMoney


class EconomicSummaryRepository:

    def __init__(self, session: Session):
        self.__session = session

    def get_economic_summary_on_month(self, month_date: date) -> EconomicSummary:
        first_date_of_month = date(day=1, month=month_date.month, year=month_date.year)
        last_date_of_month = self.__get_last_date_of_month(month_date)

        return self.__construct_economic_summary(first_date_of_month, last_date_of_month)

    @staticmethod
    def __get_last_date_of_month(month_date: date):
        if month_date.month == 12:
            next_month = 1
        else:
            next_month = month_date.month + 1

        if next_month == 1:
            first_date_next_month = date(day=1, month=1, year=month_date.year + 1)
        else:
            first_date_next_month = date(day=1, month=next_month, year=month_date.year)

        return first_date_next_month - timedelta(days=1)

    def __construct_economic_summary(self, initial_date: date, final_date: date) -> EconomicSummary:
        row_derived_from_sales = self.__get_row_with_values_derived_from_sales(initial_date, final_date)
        total_expense_row = self.__get_total_expense_row(initial_date, final_date)

        acquired_money = row_derived_from_sales['acquired_money']
        acquired_money = CUPMoney(str(acquired_money)) if acquired_money is not None else CUPMoney('0.00')

        total_cost = row_derived_from_sales['total_cost']
        total_cost = CUPMoney(str(total_cost)) if total_cost is not None else CUPMoney('0.00')

        total_expense = total_expense_row['total_expense']
        total_expense = CUPMoney(str(total_expense)) if total_expense is not None else CUPMoney('0.00')

        total_profit = acquired_money - total_cost

        return EconomicSummary(
            initial_date=initial_date,
            final_date=final_date,
            sale_quantity=row_derived_from_sales['sale_quantity'],
            acquired_money=acquired_money,
            total_cost=total_cost,
            total_profit=total_profit,
            total_expense=total_expense,
            net_profit=total_profit - total_expense
        )

    def __get_row_with_values_derived_from_sales(self, initial_date: date, final_date: date):
        query = self.__construct_query_for_values_derived_from_sales(initial_date, final_date)
        return self.__session.execute(query).first()

    @staticmethod
    def __construct_query_for_values_derived_from_sales(initial_date: date, final_date: date):
        acquired_money = func.sum(cast(Sale.price, FLOAT)).label('acquired_money')
        total_cost = func.sum(cast(Sale.cost, FLOAT)).label('total_cost')
        sale_quantity = func.count(Sale.id).label('sale_quantity')

        query = select(acquired_money, total_cost, sale_quantity) \
            .where(Sale.date >= initial_date) \
            .where(Sale.date <= final_date)
        return query

    def __get_total_expense_row(self, initial_date: date, final_date: date):
        total_expense = func.sum(cast(Expense.spent_money, FLOAT)).label('total_expense')
        return self.__session.execute(select(total_expense)
                                      .where(Expense.date >= initial_date)
                                      .where(Expense.date <= final_date)).first()

    def get_economic_summary_on_day(self, day_date: date) -> EconomicSummary:
        return self.__construct_economic_summary(day_date, day_date)
