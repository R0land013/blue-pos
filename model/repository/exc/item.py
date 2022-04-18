from model.entity.models import Item


class UniqueItemNameException(Exception):

    MSG = 'The item with name "{}" already exists.'

    def __init__(self, existing_name: str):
        self.__name = existing_name
        super().__init__(UniqueItemNameException.MSG.format(existing_name))

    def get_item_name(self):
        return self.__name


class NonExistentItemException(Exception):

    MSG = 'The item {} does not exist.'

    def __init__(self, item):
        super().__init__(NonExistentItemException.MSG.format(item))
        self.__item = item

    def get_item(self) -> Item:
        return self.__item
