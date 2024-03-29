from money import Money

from model.entity.models import Product


class UniqueProductNameException(Exception):

    MSG = 'The product with name "{}" already exists.'

    def __init__(self, existing_name: str):
        self.__name = existing_name
        super().__init__(UniqueProductNameException.MSG.format(existing_name))

    def get_product_name(self):
        return self.__name


class EmptyProductNameException(Exception):

    MSG = 'The product has an empty name'

    def __init__(self):
        super().__init__(self.MSG)


class NonExistentProductException(Exception):

    MSG = 'The product {} does not exist.'

    def __init__(self, product):
        super().__init__(NonExistentProductException.MSG.format(product))
        self.__product = product

    def get_product(self) -> Product:
        return self.__product


class InvalidProductQuantityException(Exception):

    MSG = 'The product quantity can not be negative.'

    def __init__(self):
        super().__init__(InvalidProductQuantityException.MSG)


class NoPositivePriceException(Exception):

    MSG = 'The price of a product can not be negative or zero.'

    def __init__(self):
        super().__init__(NoPositivePriceException.MSG)


class NegativeCostException(Exception):

    MSG = 'The cost can not be negative. Current value: {}'

    def __init__(self, negative_cost: Money):
        super().__init__(self.MSG.format(negative_cost))
        self.__negative_cost = negative_cost

    def get_negative_cost(self) -> Money:
        return self.__negative_cost