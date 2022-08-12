from datetime import date
from faker import Faker
from model.entity.models import Expense
from model.util.monetary_types import CUPMoney


fake = Faker()


class ExpenseGenerator:

    DEFAULT_SPENT_MONEY = CUPMoney('-1.00')

    @staticmethod
    def generate_expenses_by_quantity(quantity: int) -> list:
        expenses = []
        for _ in range(quantity):

            an_expense = ExpenseGenerator.generate_one_expense()
            expenses.append(an_expense)

        return expenses

    @staticmethod
    def generate_one_expense() -> Expense:
        an_expense = Expense()
        an_expense.name = fake.company()
        an_expense.description = fake.text()
        an_expense.spent_money = ExpenseGenerator.DEFAULT_SPENT_MONEY
        an_expense.date = date.today()

        return an_expense
