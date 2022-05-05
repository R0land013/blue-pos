from sqlalchemy import insert, update, select

from model.entity.models import Product, Sale
from sqlalchemy.orm import Session


class SaleRepository:

    def __init__(self, session: Session):
        self.__session = session

    def insert_sales(self, sale: Sale, quantity: int):
        self.__check_quantity_is_positive(quantity)

        self.__execute_insertion(sale, quantity)
        self.__execute_product_quantity_update(sale, quantity)
        self.__session.commit()

    def __check_quantity_is_positive(self, quantity: int):
        if quantity <= 0:
            raise ValueError('The quantity of sales must be positive.')

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
