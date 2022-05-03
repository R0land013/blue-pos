from sqlalchemy import TypeDecorator, Text
from money import Money


class MoneyColumn(TypeDecorator):

    impl = Text

    cache_ok = True

    def process_bind_param(self, money: Money, dialect):
        return '{} {}'.format(money.currency, money.amount)

    def process_result_value(self, money_as_str: str, dialect) -> Money:
        if money_as_str is None:
            return None
        money_as_list = money_as_str.split()
        currency = money_as_list[0]
        amount = money_as_list[1]
        return Money(amount, currency)

    def copy(self, **kw):
        return MoneyColumn()
