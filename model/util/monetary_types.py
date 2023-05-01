from money import Money


def CUPMoney(amount: str) -> Money:
    # changing "," by "." in amount string avoids Money error
    amount = amount.replace(",", ".")
    return Money(amount=amount, currency='CUP')
