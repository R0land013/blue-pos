from money import Money
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from model.entity.models import Expense
from model.repository.exc.expense import UniqueExpenseNameException, EmptyExpenseNameException, \
    NonNegativeExpenseMoneyException, NonExistentExpenseException
from model.util.monetary_types import CUPMoney


class ExpenseRepository:

    def __init__(self, session: Session):
        super().__init__()
        self.__session = session

    def insert_expense(self, new_expense: Expense):
        self.__check_money_is_negative(new_expense.spent_money)
        self.__check_name_is_not_empty_or_whitespaces(new_expense.name)
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

    def delete_expenses(self, expense_ids: list):
        self.__check_expense_ids_are_assigned_in_database(expense_ids)
        self.__execute_delete_statement(expense_ids)
        self.__session.commit()

    def __check_expense_ids_are_assigned_in_database(self, expenses_ids: list):
        found_expenses_rows = self.__session.execute(
            select(Expense.id)
            .where(Expense.id.in_(expenses_ids))).all()
        found_ids = list(map(lambda row: row.id, found_expenses_rows))

        if len(found_expenses_rows) == 0:
            raise NonExistentExpenseException(expenses_ids[0])

        for an_expense_id in expenses_ids:
            if an_expense_id not in found_ids:
                raise NonExistentExpenseException(an_expense_id)


    def __execute_delete_statement(self, expenses_ids: list):
        self.__session.execute(
            delete(Expense)
            .where(Expense.id.in_(expenses_ids))
        )

    def update_expense(self, updated_expense: Expense):
        self.__check_expense_ids_are_assigned_in_database([updated_expense.id])
        old_expense = self.__get_expense_from_database(updated_expense)
        old_expense.name = updated_expense.name
        old_expense.description = updated_expense.description
        old_expense.spent_money = updated_expense.spent_money
        old_expense.date = updated_expense.date

        self.__session.flush()
        self.__session.commit()

    def __get_expense_from_database(self, updated_expense: Expense) -> Expense:
        return self.__session.scalars(
            select(Expense).where(Expense.id == updated_expense.id)
        ).first()

    def get_all_expenses(self) -> list:
        pass