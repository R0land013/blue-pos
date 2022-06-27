from money import Money
from model.util.monetary_types import CUPMoney


def calculate_total_profit(sales: list) -> Money:
    total = CUPMoney('0')
    for a_sale in sales:
        total += a_sale.profit
    return total


def calculate_collected_money(sales: list) -> Money:
    total = CUPMoney('0')
    for a_sale in sales:
        total += a_sale.price
    return total
