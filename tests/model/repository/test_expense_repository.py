import unittest
from datetime import date, timedelta

from model.repository.exc.expense import UniqueExpenseNameException, EmptyExpenseNameException, \
    NonNegativeExpenseMoneyException, NonExistentExpenseException
from model.repository.factory import RepositoryFactory
from model.util.monetary_types import CUPMoney
from tests.util.general import TEST_DB_URL, delete_all_expenses_from_database, get_all_expenses_from_database, \
    insert_one_expense_in_database, insert_expenses_in_database
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

    def test_insert_expense_with_empty_name_raises_exception(self):
        expense = ExpenseGenerator.generate_one_expense()
        expense.name = '   '

        self.assertRaises(EmptyExpenseNameException, self.expense_repo.insert_expense, expense)

    def test_insert_expense_with_non_negative_money_raises_exception(self):
        expense = ExpenseGenerator.generate_one_expense()
        expense.spent_money = CUPMoney('0.00')

        self.assertRaises(NonNegativeExpenseMoneyException, self.expense_repo.insert_expense, expense)

    def test_delete_expenses(self):
        expenses = ExpenseGenerator.generate_expenses_by_quantity(3)
        insert_expenses_in_database(expenses)

        self.expense_repo.delete_expenses([
            expenses[0].id,
            expenses[2].id
        ])

        remaining_expenses = get_all_expenses_from_database()
        self.assertEqual(remaining_expenses, [expenses[1]])

    def test_delete_expense_with_no_assigned_id_raises_exception(self):
        self.assertRaises(NonExistentExpenseException, self.expense_repo.delete_expenses, [1])

    def test_update_expense(self):
        expense = ExpenseGenerator.generate_one_expense()
        insert_one_expense_in_database(expense)
        updated_expense = expense
        updated_expense.name = 'sillas compradas'
        updated_expense.description = 'Eran para los nuevos trabajadores'
        updated_expense.spent_money = CUPMoney('-500.00')
        updated_expense.date = date.today() - timedelta(days=1)  # yesterday

        self.expense_repo.update_expense(updated_expense)

        updated_expense_in_database = get_all_expenses_from_database()[0]
        self.assertEqual(updated_expense_in_database, updated_expense)

    def test_update_expense_with_unassigned_id_raises_exception(self):
        expense = ExpenseGenerator.generate_one_expense()
        expense.id = 1
        expense.name = 'Comprar tubos LED'

        self.assertRaises(NonExistentExpenseException, self.expense_repo.update_expense, expense)
