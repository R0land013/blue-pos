from money import Money


class CUPMoney(Money):

    def __init__(self, amount: str = '0'):
        super().__init__(amount=amount, currency='CUP')
