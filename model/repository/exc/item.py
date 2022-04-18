
class UniqueItemNameException(Exception):

    MSG = 'The item with name "{}" already exists.'

    def __init__(self, existing_name: str):
        self.__name = existing_name
        super().__init__(UniqueItemNameException.MSG.format(existing_name))

    def get_item_name(self):
        return self.__name
