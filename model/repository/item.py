from sqlalchemy.orm import Session
from model.entity.models import Item
from sqlalchemy import select

from model.repository.exc.item import UniqueItemNameException


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
        raise NotImplementedError()

    def update_item(self, old: Item, new: Item):
        raise NotImplementedError()

    def get_all_items(self) -> list:
        raise NotImplementedError()
