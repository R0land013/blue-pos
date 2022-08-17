from money import Money
from sqlalchemy import select, delete, or_
from sqlalchemy.orm import Session
from model.entity.models import Expense
from model.repository.exc.expense import UniqueExpenseNameException, EmptyExpenseNameException, \
    NonPositiveExpenseMoneyException, NonExistentExpenseException
from model.util.monetary_types import CUPMoney


class ExpenseFilter:

    def __init__(self):
        self.__minimum_date = None
        self.__maximum_date = None
        self.__id_list = None
        self.__phrase = None

    @property
    def minimum_date(self):
        return self.__minimum_date

    @minimum_date.setter
    def minimum_date(self, value):
        self.__minimum_date = value

    @property
    def maximum_date(self):
        return self.__maximum_date

    @maximum_date.setter
    def maximum_date(self, value):
        self.__maximum_date = value

    @property
    def id_list(self):
        return self.__id_list

    @id_list.setter
    def id_list(self, value: list):
        self.__id_list = value

    @property
    def phrase(self):
        return self.__phrase

    @phrase.setter
    def phrase(self, value):
        self.__phrase = value


class ExpenseRepository:

    def __init__(self, session: Session):
        super().__init__()
        self.__session = session

    def insert_expense(self, new_expense: Expense):
        self.__check_money_is_positive(new_expense.spent_money)
        self.__check_name_is_not_empty_or_whitespaces(new_expense.name)
        self.__session.add(new_expense)
        self.__session.commit()

    @staticmethod
    def __check_money_is_positive(money: Money):
        if money <= CUPMoney('0.00'):
            raise NonPositiveExpenseMoneyException(money)

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
        self.__check_name_is_not_empty_or_whitespaces(updated_expense.name)
        self.__check_money_is_positive(updated_expense.spent_money)
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
        return self.__session.scalars(select(Expense)).all()

    def get_expenses_by_filter(self, the_filter: ExpenseFilter):
        filter_query = self.__create_filter_query(the_filter)
        return self.__session.scalars(filter_query).all()

    @staticmethod
    def __create_filter_query(the_filter: ExpenseFilter):
        query = select(Expense)

        if the_filter.minimum_date is not None:
            query = query.where(Expense.date >= the_filter.minimum_date)
        if the_filter.maximum_date is not None:
            query = query.where(Expense.date <= the_filter.maximum_date)

        if the_filter.id_list is not None:
            query = query.where(Expense.id.in_(the_filter.id_list))

        if the_filter.phrase is not None:
            query = query.filter(
                or_(
                    Expense.name.ilike('%{}%'.format(the_filter.phrase)),
                    Expense.description.ilike('%{}%'.format(the_filter.phrase))
                ))

        return query
