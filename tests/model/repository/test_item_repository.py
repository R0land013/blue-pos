import unittest
from sqlalchemy import select
from model.entity.models import Item
from model.repository.factory import RepositoryFactory
from tests.util.generators.item import ItemGenerator
from tests.util.general import TEST_DB_URL
from tests.util.general import create_test_session


class TestItemRepository(unittest.TestCase):

    def tearDown(self):
        RepositoryFactory.close_session()

        with create_test_session() as session:
            statement = select(Item)
            for a_item in session.scalars(statement):
                session.delete(a_item)

    def test_items_are_inserted_successfully(self):
        fake_items = ItemGenerator.generate_items_by_quantity(3)
        item_repository = RepositoryFactory.get_item_repository(TEST_DB_URL)

        for a_item in fake_items:
            item_repository.insert_item(a_item)

        with create_test_session() as session:
            inserted_items = session.scalars(select(Item)).all()
            self.assertEqual(inserted_items, fake_items)
