import unittest
from sqlalchemy import select
from model.entity.models import Item
from model.repository.exc.product import UniqueItemNameException, NonExistentItemException
from model.repository.factory import RepositoryFactory
from tests.util.generators.product import ItemGenerator
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

        with create_test_session() as session:
            fake_item = session.scalar(select(Item))
            item_repository.delete_item(fake_item)

            items = session.scalars(select(Item)).all()
            self.assertEqual(len(items), 0)

    def test_trying_to_delete_nonexistent_item_raises_exception(self):
        fake_item = ItemGenerator.generate_one_item()
        fake_item.id = 1
        item_repository = RepositoryFactory.get_item_repository(TEST_DB_URL)

        self.assertRaises(NonExistentItemException, item_repository.delete_item, fake_item)

    def test_item_is_updated_successfully(self):
        item_repository = RepositoryFactory.get_item_repository(TEST_DB_URL)
        fake_item = ItemGenerator.generate_one_item()

        with create_test_session() as session:
            session.add(fake_item)
            session.commit()
            new_item = ItemGenerator.generate_one_item()
            new_item.id = fake_item.id

            item_repository.update_item(new_item)

            session.expunge_all()
            updated_item = session.scalar(select(Item))
            self.assertEqual(updated_item, new_item)

    def test_trying_to_update_nonexistent_item_raises_exception(self):
        item_repository = RepositoryFactory.get_item_repository(TEST_DB_URL)
        fake_item = ItemGenerator.generate_one_item()
        fake_item.id = 1

        new_item = ItemGenerator.generate_one_item()
        new_item.id = fake_item.id

        self.assertRaises(NonExistentItemException, item_repository.update_item, new_item)

    def test_trying_to_update_item_using_existent_name_raises_exception(self):
        item_repository = RepositoryFactory.get_item_repository(TEST_DB_URL)
        first_item, second_item = ItemGenerator.generate_items_by_quantity(2)

        with create_test_session() as session:
            session.add_all([first_item, second_item])
            session.commit()

            new_item = ItemGenerator.generate_one_item()
            new_item.id = first_item.id
            new_item.name = second_item.name

            self.assertRaises(UniqueItemNameException, item_repository.update_item, new_item)

    def test_trying_to_update_item_using_same_name_does_not_raise_exception(self):
        item_repository = RepositoryFactory.get_item_repository(TEST_DB_URL)
        fake_item = ItemGenerator.generate_one_item()

        with create_test_session() as session:
            session.add(fake_item)
            session.commit()
            new_item = ItemGenerator.generate_one_item()
            new_item.id = fake_item.id
            new_item.name = fake_item.name

            item_repository.update_item(new_item)

            session.expunge_all()
            updated_item = session.scalar(select(Item))
            self.assertEqual(updated_item, new_item)

    def test_get_all_items_returns_empty_list(self):
        item_repository = RepositoryFactory.get_item_repository(TEST_DB_URL)
        empty_list = []

        retrieved_list = item_repository.get_all_items()

        self.assertEqual(retrieved_list, empty_list)

    def test_get_all_items_returns_nonempty_list(self):
        item_repository = RepositoryFactory.get_item_repository(TEST_DB_URL)
        fake_items = ItemGenerator.generate_items_by_quantity(3)

        with create_test_session() as session:
            session.add_all(fake_items)
            session.commit()

            retrieved_items = item_repository.get_all_items()
            self.assertEqual(fake_items, retrieved_items)
