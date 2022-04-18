from sqlalchemy.orm import Session
from model.entity.models import Item
from sqlalchemy import select, update

from model.repository.exc.item import UniqueItemNameException, NonExistentItemException


class ItemRepository:

    def __init__(self, session: Session):
        self.session = session

    def insert_item(self, item: Item):
        self.check_name_is_not_used(item)
        self.session.add(item)
        self.session.commit()

    def check_name_is_not_used(self, item: Item):
        found_item = self.find_item_by_name(item.name)
        if found_item is not None:
            raise UniqueItemNameException(found_item.name)

    def find_item_by_name(self, name: str) -> Item:
        return self.session.scalar(
            select(Item)
            .where(Item.name.ilike(name))
        )

    def delete_item(self, item: Item):
        found_item = self.__check_item_exists(item)

        self.session.delete(found_item)
        self.session.commit()

    def __check_item_exists(self, item) -> Item:
        found_item = self.__find_item_by_id(item.id)
        if found_item is None:
            raise NonExistentItemException(item)
        return found_item

    def __find_item_by_id(self, item_id: int) -> Item:
        return self.session.scalars(
            select(Item).where(Item.id == item_id)
        ).first()

    def update_item(self, old: Item, new: Item):
        self.__check_item_exists(old)
        self.__check_name_can_be_used(old, new)

        self.session.execute(
            update(Item)
            .where(Item.id == old.id)
            .values(name=new.name, description=new.description)
        )
        self.session.commit()

    def __check_name_can_be_used(self, old: Item, new: Item):
        found_item = self.find_item_by_name(new.name)
        if found_item is not None and found_item.id != old.id:
            raise UniqueItemNameException(new.name)

    def get_all_items(self) -> list:
        raise NotImplementedError()
