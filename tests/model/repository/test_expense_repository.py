import unittest

from model.repository.exc.expense import UniqueExpenseNameException
from model.repository.factory import RepositoryFactory
from tests.util.general import TEST_DB_URL, delete_all_expenses_from_database, get_all_expenses_from_database, \
    insert_one_expense_in_database
from tests.util.generators.expense import ExpenseGenerator


class TestExpenseRepository(unittest.TestCase):

    def setUp(self):
        self.expense_repo = RepositoryFactory.get_expense_repository(TEST_DB_URL)

    def tearDown(self):
        RepositoryFactory.close_session()
        delete_all_expenses_from_database()

    def test_expenses_are_inserted(self):
        expenses = ExpenseGenerator.generate_expenses_by_quantity(3)

        for an_expense in expenses:
            self.expense_repo.insert_expense(an_expense)

        inserted_expenses = get_all_expenses_from_database()
        self.assertEqual(inserted_expenses, expenses)

    def test_insert_expense_with_already_assigned_name_ignoring_case_raises_exception(self):
        expense = ExpenseGenerator.generate_one_expense()
        expense.name = 'Compra de sillas'
        insert_one_expense_in_database(expense)

        expense.name = 'cOmPrA dE sIlLaS'
        self.assertRaises(UniqueExpenseNameException, self.expense_repo.insert_expense, expense)
