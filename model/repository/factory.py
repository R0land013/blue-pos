from model.repository.item import ItemRepository


DB_URL = 'sqlite:///data.db'


class RepositoryFactory:

    @staticmethod
    def get_item_repository(url: str = DB_URL) -> ItemRepository:
        raise NotImplementedError()
