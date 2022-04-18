import unittest
from sqlalchemy import select
from model.entity.models import Item
from model.repository.exc.item import UniqueItemNameException, NonExistentItemException
from model.repository.factory import RepositoryFactory
from tests.util.generators.item import ItemGenerator
from tests.util.general import TEST_DB_URL
from tests.util.general import create_test_session


class TestItemRepository(unittest.TestCase):

    def tearDown(self):
        RepositoryFactory.close_session()

        with create_test_session() as session:
            statement = select(Item)
            for an_item in session.scalars(statement):
                session.delete(an_item)
            session.commit()

    def test_items_are_inserted_successfully(self):
        fake_items = ItemGenerator.generate_items_by_quantity(3)
        item_repository = RepositoryFactory.get_item_repository(TEST_DB_URL)

        for an_item in fake_items:
            item_repository.insert_item(an_item)

        with create_test_session() as session:
            inserted_items = session.scalars(select(Item)).all()
            self.assertEqual(inserted_items, fake_items)

    def test_item_inserted_with_used_name_raise_exception(self):
        fake_item = ItemGenerator.generate_one_item()
        item_repository = RepositoryFactory.get_item_repository(TEST_DB_URL)

        item_repository.insert_item(fake_item)

        self.assertRaises(UniqueItemNameException, item_repository.insert_item, fake_item)

    def test_item_inserted_with_used_name_in_uppercase_raises_exception(self):
        fake_item = ItemGenerator.generate_one_item()
        item_repository = RepositoryFactory.get_item_repository(TEST_DB_URL)
        item_repository.insert_item(fake_item)

        fake_item.name = fake_item.name.upper()

        self.assertRaises(UniqueItemNameException, item_repository.insert_item, fake_item)

    def test_item_is_deleted_successfully(self):
        fake_item = ItemGenerator.generate_one_item()
        item_repository = RepositoryFactory.get_item_repository(TEST_DB_URL)
        with create_test_session() as session:
            session.add(fake_item)
            session.commit()

        item_repository.delete_item(fake_item)

        with create_test_session() as session:
            items = session.scalars(select(Item)).all()
            self.assertEqual(len(items), 0)

    def test_trying_to_delete_nonexistent_item_raises_exception(self):
        fake_item = ItemGenerator.generate_one_item()
        fake_item.id = 1
        item_repository = RepositoryFactory.get_item_repository(TEST_DB_URL)

        self.assertRaises(NonExistentItemException, item_repository.delete_item, fake_item)
