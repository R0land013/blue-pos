from sqlalchemy import select
from sqlalchemy.orm import Session
from model.entity.models import Expense
from model.repository.exc.expense import UniqueExpenseNameException, EmptyExpenseNameException


class ExpenseRepository:

    def __init__(self, session: Session):
        super().__init__()
        self.__session = session

    def insert_expense(self, new_expense: Expense):
        self.__check_name_is_not_empty_or_whitespaces(new_expense.name)
        self.__check_name_is_not_already_in_use_ignoring_case(new_expense.name)
        self.__session.add(new_expense)
        self.__session.commit()

    def __check_name_is_not_already_in_use_ignoring_case(self, name: str):
        found_expense = self.__session.scalar(select(Expense)
                                              .where(Expense.name.ilike(name)))
        if found_expense is not None:
            raise UniqueExpenseNameException(name)

    @staticmethod
    def __check_name_is_not_empty_or_whitespaces(name: str):
        if name.isspace() or name == '':
            raise EmptyExpenseNameException()

    def delete_expenses(self, expense_ids: list):
        pass

    def update_expense(self, updated_expense: Expense):
        pass

    def get_all_expenses(self) -> list:
        pass