import unittest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import select
from model.entity.models import Item
from model.repository.factory import RepositoryFactory
from tests.util.generators.item import ItemGenerator


class TestItemRepository(unittest.TestCase):

    def setUp(self):
        self.db_url = 'sqlite:///test.db'

    def tearDown(self):
        RepositoryFactory.close_session()
        engine = create_engine(self.db_url)
        statement = select(Item)
        with Session(engine) as session:
            for a_item in session.scalars(statement):
                session.delete(a_item)

    def test_items_are_inserted_successfully(self):
        fake_items = ItemGenerator.generate_items_by_quantity(3)
        item_repository = RepositoryFactory.get_item_repository(self.db_url)

        for a_item in fake_items:
            item_repository.insert_item(a_item)

        with Session(create_engine(self.db_url)) as session:
            inserted_items = session.scalars(select(Item)).all()
            self.assertEqual(inserted_items, fake_items)
