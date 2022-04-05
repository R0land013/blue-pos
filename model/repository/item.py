from model.entity.models import Item


class ItemRepository:

    def __init__(self):
        pass

    def insert_item(self, item: Item):
        raise NotImplementedError()

    def delete_item(self, item: Item):
        raise NotImplementedError()

    def update_item(self, old: Item, new: Item):
        raise NotImplementedError()

    def get_all_items(self) -> list:
        raise NotImplementedError()
