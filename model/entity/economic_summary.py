from datetime import date
from money import Money


class EconomicSummary:

    def __init__(self,
                 initial_date: date,
                 final_date: date,
                 sale_quantity: int,
                 acquired_money: Money,
                 total_cost: Money,
                 total_profit: Money,
                 total_expense: Money,
                 net_profit: Money):

        self.__initial_date = initial_date
        self.__final_date = final_date
        self.__sale_quantity = sale_quantity
        self.__acquired_money = acquired_money
        self.__total_cost = total_cost
        self.__total_profit = total_profit
        self.__total_expense = total_expense
        self.__net_profit = net_profit

    def __eq__(self, other):
        return (self.__initial_date == other.initial_date
                and self.__final_date == other.final_date
                and self.__sale_quantity == other.sale_quantity
                and self.__acquired_money == other.acquired_money
                and self.__total_cost == other.total_cost
                and self.__total_profit == other.total_profit
                and self.__total_expense == other.total_expense
                and self.__net_profit == other.net_profit)

    def __repr__(self):
        return self.__str__()

    def __str__(self) -> str:
        return f'EconomicSummary(initial_date: {self.__initial_date}, final_date:{self.__final_date}, ' \
               f'sale_quantity: {self.__sale_quantity}, acquired_money: {self.__acquired_money}, ' \
               f'total_cost: {self.__total_cost}, total_profit: {self.__total_profit}, ' \
               f'total_expense: {self.__total_expense}, net_profit: {self.__net_profit})'


    @property
    def initial_date(self) -> date:
        return self.__initial_date

    @property
    def final_date(self) -> date:
        return self.__final_date

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
    def total_expense(self) -> Money:
        return self.__total_expense

    @property
    def net_profit(self) -> Money:
        return self.__net_profit
