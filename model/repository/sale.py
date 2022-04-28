from model.entity.models import Product, Sale
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import insert


class SaleRepository:

    def __init__(self, session: Session):
        self.__session = session

    def insert_sale(self, product: Product, sale_date: date):
        self.__execute_insert_clause(product, sale_date)
        self.__session.commit()

    def __execute_insert_clause(self, product: Product, sale_date: date):
        self.__session.execute(
            insert(Sale)
                .values(
                product_id=product.id,
                price=product.price,
                profit=product.profit,
                date=sale_date
            )
        )

    def delete_sale(self, sale: Sale):
        raise NotImplementedError()

    def update_sale(self, sale: Sale):
        raise NotImplementedError()

    def get_all_sales(self) -> list:
        raise NotImplementedError()
