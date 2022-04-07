import unittest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import select
from model.entity.models import Item
from model.repository.factory import RepositoryFactory
from tests.util.generators.item import ItemGenerator


class TestItemRepository(unittest.TestCase):

    def setUp(self) -> None:
        self.db_url = 'sqlite:///test.db'

    def tearDown(self) -> None:
        engine = create_engine(self.db_url)
        statement = select(Item)
        with Session(engine) as session:
            for a_item in session.scalars(statement):
                session.delete(a_item)

    def test_items_are_inserted_successfully(self):
        item_repository = RepositoryFactory.get_item_repository(self.db_url)
        fake_items = ItemGenerator.generate_items_by_quantity(3)
        for a_item in fake_items:
            item_repository.insert_item(a_item)

        with Session(create_engine(self.db_url)) as session:
            inserted_items = session.scalars(select(Item))
            self.assertEqual(fake_items, inserted_items)
