from datetime import date
from money import Money


class ReportStatistic:

    def __init__(self, sale_quantity: int, paid_money: Money, cost_money: Money,
                 total_expenses: Money, initial_date: date, final_date: date):
        self.__sale_quantity = sale_quantity
        self.__paid_money = paid_money
        self.__cost_money = cost_money
        self.__total_expenses = total_expenses
        self.__initial_date = initial_date
        self.__final_date = final_date

    def __eq__(self, other):
        return (self.__sale_quantity == other.sale_quantity() and self.__paid_money == other.paid_money()
                and self.__cost_money == other.cost_money() and self.__total_expenses == other.total_expenses()
                and self.__initial_date == other.initial_date() and self.__final_date == other.final_date())

    def __str__(self):
        return 'ReportStatistic( sale_quantity: {}, paid_money: {}, cost_money: {}, profit_money: {},' \
               'total_expenses: {}, net_profit: {}, initial_date: {}, final_date: {})'.format(
                self.__sale_quantity, self.__paid_money, self.__cost_money, self.profit_money(),
                self.__total_expenses, self.net_profit(), self.__initial_date, self.__final_date
                )

    def __repr__(self):
        return self.__str__()

    def sale_quantity(self) -> int:
        return self.__sale_quantity

    def paid_money(self) -> Money:
        return self.__paid_money

    def cost_money(self) -> Money:
        return self.__cost_money

    def profit_money(self) -> Money:
        return self.__paid_money - self.__cost_money

    def total_expenses(self) -> Money:
        return self.__total_expenses

    def net_profit(self) -> Money:
        return self.profit_money() - self.__total_expenses

    def initial_date(self) -> date:
        return self.__initial_date

    def final_date(self) -> date:
        return self.__final_date
