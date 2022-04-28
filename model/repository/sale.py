from model.entity.models import Product, Sale
from datetime import date
from sqlalchemy.orm import Session


class SaleRepository:

    def __init__(self, session: Session):
        self.__session = session

    def insert_sale(self, product: Product, sale_date: date):
        raise NotImplementedError()

    def delete_sale(self, sale: Sale):
        raise NotImplementedError()

    def update_sale(self, sale: Sale):
        raise NotImplementedError()

    def get_all_sales(self) -> list:
        raise NotImplementedError()
