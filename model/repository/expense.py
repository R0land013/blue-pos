from money import Money
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from model.entity.models import Expense
from model.repository.exc.expense import UniqueExpenseNameException, EmptyExpenseNameException, \
    NonNegativeExpenseMoneyException
from model.util.monetary_types import CUPMoney


class ExpenseRepository:

    def __init__(self, session: Session):
        super().__init__()
        self.__session = session

    def insert_expense(self, new_expense: Expense):
        self.__check_money_is_negative(new_expense.spent_money)
        self.__check_name_is_not_empty_or_whitespaces(new_expense.name)
        self.__check_name_is_not_already_in_use_ignoring_case(new_expense.name)
        self.__session.add(new_expense)
        self.__session.commit()

    @staticmethod
    def __check_money_is_negative(money: Money):
        if money >= CUPMoney('0.00'):
            raise NonNegativeExpenseMoneyException(money)

    @staticmethod
    def __check_name_is_not_empty_or_whitespaces(name: str):
        if name.isspace() or name == '':
            raise EmptyExpenseNameException()

    def __check_name_is_not_already_in_use_ignoring_case(self, name: str):
        found_expense = self.__session.scalar(select(Expense)
                                              .where(Expense.name.ilike(name)))
        if found_expense is not None:
            raise UniqueExpenseNameException(name)

    def delete_expenses(self, expense_ids: list):
        self.__execute_delete_statement(expense_ids)
        self.__session.commit()

    def __execute_delete_statement(self, expenses_ids: list):
        self.__session.execute(
            delete(Expense)
            .where(Expense.id.in_(expenses_ids))
        )

    def update_expense(self, updated_expense: Expense):
        pass

    def get_all_expenses(self) -> list:
        pass