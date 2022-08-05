from money import Money

from model.entity.models import Product


class UniqueProductNameException(Exception):

    MSG = 'The product with name "{}" already exists.'

    def __init__(self, existing_name: str):
        self.__name = existing_name
        super().__init__(UniqueProductNameException.MSG.format(existing_name))

    def get_product_name(self):
        return self.__name


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


class NegativeProfitException(Exception):

    MSG = 'The profit of a product can not be negative.'

    def __init__(self):
        super().__init__(NegativeProfitException.MSG)


class TooMuchProfitException(Exception):

    MSG = 'The profit cannot be higher than price. {} > {}'

    def __init__(self, price: Money, profit: Money):
        super().__init__(self.MSG.format(str(profit), str(price)))
        self.__price = price
        self.__profit = profit

    def get_price(self) -> Money:
        return self.__price

    def get_profit(self) -> Money:
        return self.__profit
