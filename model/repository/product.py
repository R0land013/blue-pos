from sqlalchemy.orm import Session
from model.entity.models import Item
from sqlalchemy import select, update

from model.repository.exc.product import UniqueItemNameException, NonExistentItemException


class ItemRepository:

    def __init__(self, session: Session):
        self.__session = session

    def insert_item(self, item: Item):
        self.__check_name_is_not_used(item)
        self.__session.add(item)
        self.__session.commit()

    def __check_name_is_not_used(self, item: Item):
        found_item = self.__find_item_by_name(item.name)
        if found_item is not None:
            raise UniqueItemNameException(found_item.name)

    def __find_item_by_name(self, name: str) -> Item:
        return self.__session.scalar(
            select(Item)
            .where(Item.name.ilike(name))
        )

    def delete_item(self, item: Item):
        found_item = self.__check_item_exists(item)

        self.__session.delete(found_item)
        self.__session.commit()

    def __check_item_exists(self, item) -> Item:
        found_item = self.__find_item_by_id(item.id)
        if found_item is None:
            raise NonExistentItemException(item)
        return found_item

    def __find_item_by_id(self, item_id: int) -> Item:
        return self.__session.scalars(
            select(Item).where(Item.id == item_id)
        ).first()

    def update_item(self, new: Item):
        old = self.__check_item_exists(new)
        self.__check_name_can_be_used(old, new)

        old.name = new.name
        old.description = new.description

        self.__session.flush()
        self.__session.commit()

    def __check_name_can_be_used(self, old: Item, new: Item):
        found_item = self.__find_item_by_name(new.name)
        if found_item is not None and found_item.id != old.id:
            raise UniqueItemNameException(new.name)

    def get_all_items(self) -> list:
        return self.__session.scalars(select(Item)).all()
