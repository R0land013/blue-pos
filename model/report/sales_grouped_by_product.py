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

    def __str__(self):
        return 'SalesGroupedByProduct(product_id: {}, product_name: \'{}\', ' \
               'sale_quantity: {}, acquired_money: {}, total_cost: {}, ' \
               'total_profit: {}, initial_date: {}, final_date: {})'.format(
                self.__product_id, self.__product_name, self.__sale_quantity,
                self.__acquired_money, self.__total_cost, self.__total_profit,
                self.__initial_date, self.__final_date
                )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other) -> bool:
        return (self.__product_id == other.product_id
                and self.__product_name == other.product_name
                and self.__sale_quantity == other.sale_quantity
                and self.__acquired_money == other.acquired_money
                and self.__total_cost == other.total_cost
                and self.__total_profit == other.total_profit
                and self.__initial_date == other.initial_date
                and self.__final_date == other.final_date)

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
