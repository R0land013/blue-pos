from datetime import date
from money import Money


class ReportStatistic:

    def __init__(self, sale_quantity: int, paid_money: Money, profit_money: Money,
                 initial_date: date, final_date: date):
        pass

    def sale_quantity(self) -> int:
        pass

    def paid_money(self) -> Money:
        pass

    def profit_money(self) -> Money:
        pass

    def initial_date(self) -> date:
        pass

    def final_date(self) -> date:
        pass
