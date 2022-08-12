

class UniqueExpenseNameException(Exception):

    MSG = 'The name \'{}\' is already in use by an expense.'

    def __init__(self, name: str):
        super().__init__(self.MSG.format(name))
        self.__name = name

    def get_name(self) -> str:
        return self.__name


class EmptyExpenseNameException(Exception):

    def __init__(self):
        super().__init__('The name of an expense can not be empty or empty spaces')
