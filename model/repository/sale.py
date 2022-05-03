from model.entity.models import Product, Sale
from sqlalchemy.orm import Session


class SaleRepository:

    def __init__(self, session: Session):
        self.__session = session

    def insert_sale(self, sale: Sale):
        self.__session.add(sale)
        self.__session.commit()

    def delete_sale(self, sale: Sale):
        raise NotImplementedError()

    def update_sale(self, sale: Sale):
        raise NotImplementedError()

    def get_all_sales(self) -> list:
        raise NotImplementedError()
