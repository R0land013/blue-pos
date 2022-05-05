from sqlalchemy import insert

from model.entity.models import Product, Sale
from sqlalchemy.orm import Session


class SaleRepository:

    def __init__(self, session: Session):
        self.__session = session

    def insert_sales(self, sale: Sale, quantity: int):
        self.__execute_insertion(sale, quantity)
        self.__session.commit()

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

    def delete_sale(self, sale: Sale):
        raise NotImplementedError()

    def update_sale(self, sale: Sale):
        raise NotImplementedError()

    def get_all_sales(self) -> list:
        raise NotImplementedError()
