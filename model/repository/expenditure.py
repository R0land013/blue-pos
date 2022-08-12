from sqlalchemy.orm import Session
from model.entity.models import Expense


class ExpenseRepository:

    def __init__(self, session: Session):
        super().__init__()
        self.__session = session

    def insert_expense(self, new_expense: Expense):
        pass

    def delete_expenses(self, expense_ids: list):
        pass

    def update_expense(self, updated_expense: Expense):
        pass

    def get_all_expenses(self) -> list:
        pass