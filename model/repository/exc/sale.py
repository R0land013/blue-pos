

class NoEnoughProductQuantityException(Exception):

    MSG = 'No enough products. Remaining: {}.'

    def __init__(self, remaining_quantity):
        self.__remaining_quantity = remaining_quantity
        super().__init__(NoEnoughProductQuantityException.MSG.format(remaining_quantity))

    def get_remaining_quantity(self) -> int:
        return self.__remaining_quantity


class NonExistentSaleException(Exception):

    MSG = 'The sale {} does not exist.'

    def __init__(self, sale):
        super().__init__(NonExistentSaleException.MSG.format(sale))
        self.__sale = sale

    def get_sale(self):
        return self.__sale


class ChangeProductIdInSaleException(Exception):

    MSG = 'The product id of a sale can not be changed.'

    def __init__(self):
        super().__init__(ChangeProductIdInSaleException.MSG)
