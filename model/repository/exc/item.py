
class UniqueItemNameException(Exception):

    MSG = 'The item with name "{}" already exists.'

    def __init__(self, existing_name: str):
        super().__init__(UniqueItemNameException.MSG.format(existing_name))
