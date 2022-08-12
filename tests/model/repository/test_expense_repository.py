import unittest
from model.repository.factory import RepositoryFactory
from tests.util.general import TEST_DB_URL, delete_all_expenses_from_database


class TestExpenseRepository(unittest.TestCase):

    def setUp(self):
        self.expense_repository = RepositoryFactory.get_expense_repository(TEST_DB_URL)

    def tearDown(self):
        RepositoryFactory.close_session()
        delete_all_expenses_from_database()