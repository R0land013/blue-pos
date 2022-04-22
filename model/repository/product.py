from sqlalchemy.orm import Session
from model.entity.models import Product
from sqlalchemy import select, update

from model.repository.exc.product import UniqueProductNameException, NonExistentProductException


class ProductRepository:

    def __init__(self, session: Session):
        self.__session = session

    def insert_product(self, product: Product):
        self.__check_name_is_not_used(product)
        self.__session.add(product)
        self.__session.commit()

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