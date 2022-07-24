from datetime import date
from money import Money


class ReportStatistic:

    def __init__(self, sale_quantity: int, paid_money: Money, profit_money: Money,
                 initial_date: date, final_date: date):
        self.__sale_quantity = sale_quantity
        self.__paid_money = paid_money
        self.__profit_money = profit_money
        self.__initial_date = initial_date
        self.__final_date = final_date

    def sale_quantity(self) -> int:
        return self.__sale_quantity

    def paid_money(self) -> Money:
        return self.__paid_money

    def profit_money(self) -> Money:
        return self.__profit_money

    def initial_date(self) -> date:
        return self.__initial_date

    def final_date(self) -> date:
        return self.__final_date
