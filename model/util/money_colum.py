from sqlalchemy import TypeDecorator, Text, type_coerce, Numeric, NUMERIC
from money import Money
from sqlalchemy.sql import operators


class MoneyColumn(TypeDecorator):

    impl = Text

    cache_ok = True

    # comparator_factory = MoneyComparator

    # def coerce_compared_value(self, op, value):
    #     return type_coerce(value, NUMERIC)

    def process_bind_param(self, money: Money, dialect):
        return '{}'.format(money.amount)

    def process_result_value(self, money_as_str: str, dialect) -> Money:
        if money_as_str is None:
            return None

        return Money(money_as_str, 'CUP')

    def copy(self, **kw):
        return MoneyColumn()

