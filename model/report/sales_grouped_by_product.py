from datetime import date
from money import Money


class SalesGroupedByProduct:

    def __init__(self, product_id: int, product_name: str, sale_quantity: int,
                 acquired_money: Money, total_cost: Money, total_profit: Money,
                 initial_date: date, final_date: date):

        self.__product_id: int = product_id
        self.__product_name: str = product_name
        self.__sale_quantity: int = sale_quantity
        self.__acquired_money: Money = acquired_money
        self.__total_cost: Money = total_cost
        self.__total_profit: Money = total_profit
        self.__initial_date: date = initial_date
        self.__final_date: date = final_date

    @property
    def product_id(self) -> int:
        return self.__product_id

    @property
    def product_name(self) -> str:
        return self.__product_name

    @property
    def sale_quantity(self) -> int:
        return self.__sale_quantity

    @property
    def acquired_money(self) -> Money:
        return self.__acquired_money

    @property
    def total_cost(self) -> Money:
        return self.__total_cost

    @property
    def total_profit(self) -> Money:
        return self.__total_profit

    @property
    def initial_date(self) -> date:
        return self.__initial_date

    @property
    def final_date(self) -> date:
        return self.__final_date
