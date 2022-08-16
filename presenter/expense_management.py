from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent

from model.entity.models import Expense
from model.repository.factory import RepositoryFactory
from presenter.expense_form import ExpenseFormPresenter
from presenter.util.thread_worker import PresenterThreadWorker
from view.expense_management import ExpenseManagementView


class ExpenseManagementPresenter(AbstractPresenter):

    def _on_initialize(self):
        self._set_view(ExpenseManagementView(self))
        self.__expense_repo = RepositoryFactory.get_expense_repository()
        self.__expenses = []

    def close_presenter(self):
        self._close_this_presenter()

    def on_view_shown(self):
        self.__execute_thread_to_fill_table()

    def __execute_thread_to_fill_table(self):
        self.thread = PresenterThreadWorker(self.__load_expenses)
        self.thread.when_started.connect(self.__disable_view_and_show_loading_message)
        self.thread.when_finished.connect(self.__fill_table)
        self.thread.when_finished.connect(self.__set_view_available_and_show_no_message)
        self.thread.start()

    def __load_expenses(self, thread: PresenterThreadWorker):
        self.__expenses = self.__expense_repo.get_all_expenses()

    def __disable_view_and_show_loading_message(self):
        self.get_view().disable_all_gui(True)
        self.get_view().set_status_bar_message('Cargando datos...')

    def __fill_table(self):
        for an_expense in self.__expenses:
            self.__add_expense_to_table(an_expense)
        self.get_view().resize_table_columns_to_contents()

    def __add_expense_to_table(self, an_expense: Expense):
        self.get_view().add_empty_row_at_the_end_of_table()
        row = self.get_view().get_last_row_index()
        self.__set_table_row_by_expense(row, an_expense)

    def __set_table_row_by_expense(self, row: int, an_expense: Expense):
        view = self.get_view()
        view.set_cell_in_table(row, ExpenseManagementView.ID_COLUMN, an_expense.id)
        view.set_cell_in_table(row, ExpenseManagementView.NAME_COLUMN, an_expense.name)
        view.set_cell_in_table(row, ExpenseManagementView.SPENT_MONEY_COLUMN, an_expense.spent_money)
        view.set_cell_in_table(row, ExpenseManagementView.DATE_COLUMN, an_expense.date)

    def __set_view_available_and_show_no_message(self):
        self.get_view().disable_all_gui(False)
        self.get_view().set_status_bar_message('')

    def open_expense_form_presenter_to_add_new_expense(self):
        intent = Intent(ExpenseFormPresenter)
        intent.set_action(ExpenseFormPresenter.CREATE_NEW_EXPENSE_ACTION)
        intent.use_new_window(True)
        intent.use_modal(True)
        self._open_other_presenter(intent)

    def on_view_discovered_with_result(self, action: str, result_data: dict, result: str):
        if result == ExpenseFormPresenter.NEW_EXPENSE_CREATED_RESULT:
            self.__add_new_expense_to_table(result_data)

    def __add_new_expense_to_table(self, result_data: dict):
        new_expense = result_data[ExpenseFormPresenter.NEW_EXPENSE_RESULT_DATA]
        self.__add_expense_to_table(new_expense)
        self.get_view().resize_table_columns_to_contents()