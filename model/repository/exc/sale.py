

class NoEnoughProductQuantityException(Exception):

    MSG = 'No enough products. Remaining: {}.'

    def __init__(self, remaining_quantity):
        self.__remaining_quantity = remaining_quantity
        super().__init__(NoEnoughProductQuantityException.MSG.format(remaining_quantity))

    def get_remaining_quantity(self) -> int:
        return self.__remaining_quantity
