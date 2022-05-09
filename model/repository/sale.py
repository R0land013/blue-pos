from sqlalchemy import insert, update, select

from model.entity.models import Product, Sale
from sqlalchemy.orm import Session

from model.repository.exc.product import NonExistentProductException, NoPositivePriceException, NegativeProfitException
from model.repository.exc.sale import NoEnoughProductQuantityException
from model.util.monetary_types import CUPMoney


class SaleRepository:

    def __init__(self, session: Session):
        self.__session = session

    def insert_sales(self, sale: Sale, quantity: int):
        self.__check_quantity_is_positive(quantity)
        self.__check_price_is_positive(sale)
        self.__check_profit_is_not_negative(sale)
        product = self.__get_product_by_id(sale.product_id)
        self.__check_product_exists(product, sale.product_id)
        self.__check_there_are_enough_products(product, quantity)

        self.__execute_insertion(sale, quantity)
        self.__execute_product_quantity_update(sale, quantity)
        self.__session.commit()

    def __check_quantity_is_positive(self, quantity: int):
        if quantity <= 0:
            raise ValueError('The quantity of sales must be positive.')

    def __check_price_is_positive(self, sale: Sale):
        if not sale.price > CUPMoney('0.00'):
            raise NoPositivePriceException()

    def __check_profit_is_not_negative(self, sale: Sale):
        if sale.profit < CUPMoney('0.00'):
            raise NegativeProfitException()

    def __get_product_by_id(self, product_id: int) -> Product:
        return self.__session.scalar(select(Product).where(Product.id == product_id))

    def __check_product_exists(self, product: Product, product_id: int):
        if product is None:
            nonexistent_product = Product()
            nonexistent_product.id = product_id
            raise NonExistentProductException(nonexistent_product)

    def __check_there_are_enough_products(self, product: Product, sale_quantity: int):
        if product.quantity - sale_quantity < 0:
            raise NoEnoughProductQuantityException(product.quantity)

    def __execute_insertion(self, sale: Sale, quantity: int):
        for i in range(quantity):
            self.__session.execute(
                insert(Sale)
                .values(
                    product_id=sale.product_id,
                    date=sale.date,
                    price=sale.price,
                    profit=sale.profit
                )
            )

    def __execute_product_quantity_update(self, sale: Sale, sale_quantity: int):
        product = self.__session.scalar(select(Product).where(Product.id == sale.product_id))

        self.__session.execute(
            update(Product)
            .where(Product.id == sale.product_id)
            .values(quantity=product.quantity - sale_quantity)
        )

    def delete_sale(self, sale: Sale):
        raise NotImplementedError()

    def update_sale(self, sale: Sale):
        raise NotImplementedError()

    def get_all_sales(self) -> list:
        raise NotImplementedError()
