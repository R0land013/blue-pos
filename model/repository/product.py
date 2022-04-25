from sqlalchemy.orm import Session
from model.entity.models import Product
from sqlalchemy import select

from model.repository.exc.product import UniqueProductNameException, NonExistentProductException, \
    InvalidProductQuantityException, InvalidPriceForProductException, NegativeProfitForProductException
from model.util.monetary_types import CUPMoney


class ProductFilter:

    def __init__(self):
        self.id = None
        self.name = None
        self.description = None
        self.__less_than_price = None
        self.__more_than_price = None
        self.__less_than_profit = None
        self.__more_than_profit = None
        self.__less_than_quantity = None
        self.__more_than_quantity = None

    @property
    def less_than_price(self):
        return self.__less_than_price

    @less_than_price.setter
    def less_than_price(self, value: CUPMoney):
        self.__check_price_correctness(value)
        self.__less_than_price = value

    def __check_price_correctness(self, value: CUPMoney):
        if value is not None and value <= CUPMoney('0'):
            raise InvalidPriceForProductException()

    @property
    def more_than_price(self):
        return self.__more_than_price

    @more_than_price.setter
    def more_than_price(self, value: CUPMoney):
        self.__check_price_correctness(value)
        self.__more_than_price = value

    @property
    def less_than_profit(self):
        return self.__less_than_profit

    @less_than_profit.setter
    def less_than_profit(self, value: CUPMoney):
        self.__check_profit_correctness(value)
        self.__less_than_profit = value

    def __check_profit_correctness(self, value: CUPMoney):
        if value is not None and value < CUPMoney('0'):
            raise NegativeProfitForProductException()

    @property
    def more_than_profit(self):
        return self.__more_than_profit

    @more_than_profit.setter
    def more_than_profit(self, value: CUPMoney):
        self.__check_profit_correctness(value)
        self.__more_than_profit = value

    @property
    def less_than_quantity(self):
        return self.__less_than_quantity

    @less_than_quantity.setter
    def less_than_quantity(self, value: int):
        self.__check_quantity_correctness(value)
        self.__less_than_quantity = value

    def __check_quantity_correctness(self, value: int):
        if value is not None and value < 0:
            raise InvalidProductQuantityException()

    @property
    def more_than_quantity(self):
        return self.__more_than_quantity

    @more_than_quantity.setter
    def more_than_quantity(self, value: int):
        self.__check_quantity_correctness(value)
        self.__more_than_quantity = value


class ProductRepository:

    def __init__(self, session: Session):
        self.__session = session

    def insert_product(self, product: Product):
        self.__check_correctness_of_quantity(product)
        self.__check_correctness_of_price(product)
        self.__check_correctness_of_profit(product)
        self.__check_name_is_not_used(product)

        self.__session.add(product)
        self.__session.commit()

    def __check_correctness_of_quantity(self, product: Product):
        if product.quantity < 0:
            raise InvalidProductQuantityException()

    def __check_correctness_of_price(self, product: Product):
        if product.price <= CUPMoney('0.00'):
            raise InvalidPriceForProductException()

    def __check_correctness_of_profit(self, product: Product):
        if product.profit < CUPMoney('0.00'):
            raise NegativeProfitForProductException()

    def __check_name_is_not_used(self, product: Product):
        found_product = self.__find_product_by_name(product.name)
        if found_product is not None:
            raise UniqueProductNameException(found_product.name)

    def __find_product_by_name(self, name: str) -> Product:
        return self.__session.scalar(
            select(Product)
            .where(Product.name.ilike(name))
        )

    def delete_product(self, product: Product):
        found_product = self.__check_product_exists(product)

        self.__session.delete(found_product)
        self.__session.commit()

    def __check_product_exists(self, product) -> Product:
        found_product = self.__find_product_by_id(product.id)
        if found_product is None:
            raise NonExistentProductException(product)
        return found_product

    def __find_product_by_id(self, product_id: int) -> Product:
        return self.__session.scalars(
            select(Product).where(Product.id == product_id)
        ).first()

    def update_product(self, new: Product):
        self.__check_correctness_of_quantity(new)
        self.__check_correctness_of_price(new)
        self.__check_correctness_of_profit(new)
        old = self.__check_product_exists(new)
        self.__check_name_can_be_used(old, new)

        old.name = new.name
        old.description = new.description

        self.__session.flush()
        self.__session.commit()

    def __check_name_can_be_used(self, old: Product, new: Product):
        found_product = self.__find_product_by_name(new.name)
        if found_product is not None and found_product.id != old.id:
            raise UniqueProductNameException(new.name)

    def get_all_products(self) -> list:
        return self.__session.scalars(select(Product)).all()

    def get_products_by_filter(self, the_filter: ProductFilter) -> list:
        filter_query = self.__create_query(the_filter)
        return self.__session.scalars(filter_query).all()

    def __create_query(self, the_filter: ProductFilter):
        query = select(Product)
        if the_filter.id is not None:
            query = query.where(Product.id == the_filter.id)

        if the_filter.name is not None:
            query = query.where(Product.name.ilike('%{}%'.format(the_filter.name)))

        if the_filter.description is not None:
            query = query.where(Product.description.ilike('%{}%'.format(the_filter.description)))

        if the_filter.more_than_price is not None:
            query = query.where(Product.price >= the_filter.more_than_price)
        if the_filter.less_than_price is not None:
            query = query.where(Product.price <= the_filter.less_than_price)

        if the_filter.more_than_profit is not None:
            query = query.where(Product.profit >= the_filter.more_than_profit)
        if the_filter.less_than_profit is not None:
            query = query.where(Product.profit <= the_filter.less_than_profit)
        return query
