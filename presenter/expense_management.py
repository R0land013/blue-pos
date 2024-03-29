from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent

from model.entity.models import Expense
from model.repository.expense import ExpenseFilter
from model.repository.factory import RepositoryFactory
from presenter.expense_filter import ExpenseFilterPresenter
from presenter.expense_form import ExpenseFormPresenter
from presenter.util.thread_worker import PresenterThreadWorker
from view.expense_management import ExpenseManagementView


class ExpenseManagementPresenter(AbstractPresenter):

    def _on_initialize(self):
        self._set_view(ExpenseManagementView(self))
        self.__expense_repo = RepositoryFactory.get_expense_repository()
        self.__expenses = []
        self.__expense_filter: ExpenseFilter = None

    def close_presenter(self):
        self._close_this_presenter()

    def get_default_window_title(self) -> str:
        return 'Blue POS - Gestión de gastos'

    def on_view_shown(self):
        self.__execute_thread_to_fill_table()

    def __execute_thread_to_fill_table(self):
        self.thread = PresenterThreadWorker(self.__load_expenses)

        self.thread.when_started.connect(self.__disable_view_and_show_loading_message)

        self.thread.when_finished.connect(self.__fill_table)
        self.thread.when_finished.connect(self.get_view().sort_table_rows)
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

        elif result == ExpenseFormPresenter.UPDATED_EXPENSE_RESULT:
            self.__update_expense_on_table(result_data)

        elif result == ExpenseFilterPresenter.CREATED_EXPENSE_FILTER_RESULT:
            self.__execute_thread_to_filter_expenses(result_data)

    def __add_new_expense_to_table(self, result_data: dict):
        new_expense = result_data[ExpenseFormPresenter.NEW_EXPENSE_RESULT_DATA]

        if self.__expense_filter is None or self.__is_it_match_filter_values(new_expense):
            self.__add_expense_to_table(new_expense)
            self.get_view().sort_table_rows()
            self.get_view().resize_table_columns_to_contents()
        
        self.get_view().show_success_toast_message('Nuevo gasto creado')

    def __is_it_match_filter_values(self, expense: Expense) -> bool:
        return self.__expense_filter is not None and self.__expense_filter.is_it_match(expense)

    def open_expense_form_presenter_to_update_expense(self):
        intent = Intent(ExpenseFormPresenter)
        expense_to_update = self.__get_selected_expense_to_update()
        data = {ExpenseFormPresenter.EXPENSE_TO_UPDATE: expense_to_update}
        intent.set_data(data)
        intent.set_action(ExpenseFormPresenter.UPDATE_EXPENSE_ACTION)
        intent.use_new_window(True)
        intent.use_modal(True)
        self._open_other_presenter(intent)

    def __get_selected_expense_to_update(self) -> Expense:
        the_filter = ExpenseFilter()
        the_filter.id_list = self.get_view().get_all_selected_expense_ids()
        return self.__expense_repo.get_expenses_by_filter(the_filter)[0]

    def __update_expense_on_table(self, result_data: dict):
        row = self.get_view().get_selected_row_index()
        updated_expense = result_data[ExpenseFormPresenter.UPDATED_EXPENSE_RESULT_DATA]

        if self.__expense_filter is None or self.__is_it_match_filter_values(updated_expense):
            self.__set_table_row_by_expense(row, updated_expense)
            self.get_view().sort_table_rows()
            self.get_view().resize_table_columns_to_contents()

        elif not self.__is_it_match_filter_values(updated_expense):
            self.get_view().delete_selected_rows_from_table()

        self.get_view().show_success_toast_message('Gasto actualizado')

    def execute_thread_to_delete_selected_expenses(self):
        if self.get_view().ask_user_to_confirm_deleting_expenses():
            self.__selected_ids = self.get_view().get_all_selected_expense_ids()
            self.thread = PresenterThreadWorker(self.__delete_selected_expenses)

            self.thread.when_started.connect(lambda: self.get_view().disable_all_gui(True))
            self.thread.when_started.connect(lambda: self.get_view().set_status_bar_message('Procesando...'))

            self.thread.when_finished.connect(lambda: self.get_view().delete_selected_rows_from_table())
            self.thread.when_finished.connect(lambda: self.get_view().disable_all_gui(False))
            self.thread.when_finished.connect(lambda: self.get_view().set_status_bar_message(''))
            self.thread.when_finished.connect(
                lambda: self.get_view().show_success_toast_message('Eliminación completada'))

            self.thread.start()

    def __delete_selected_expenses(self, thread: PresenterThreadWorker):
        self.__expense_repo.delete_expenses(self.__selected_ids)

    def open_expense_filter_presenter(self):
        intent = Intent(ExpenseFilterPresenter)
        data = {ExpenseFilterPresenter.EXPENSE_FILTER_DATA: self.__expense_filter}
        intent.set_data(data)
        intent.use_new_window(True)
        intent.use_modal(True)
        self._open_other_presenter(intent)

    def __execute_thread_to_filter_expenses(self, result_data: dict):
        self.__expense_filter = result_data[ExpenseFilterPresenter.CREATED_EXPENSE_FILTER_DATA]
        self.thread = PresenterThreadWorker(self.__filter_expenses)

        self.thread.when_started.connect(lambda: self.get_view().set_status_bar_message('Filtrando...'))
        self.thread.when_started.connect(lambda: self.get_view().disable_all_gui(True))

        self.thread.when_finished.connect(self.get_view().clean_table)
        self.thread.when_finished.connect(self.__fill_table)
        self.thread.when_finished.connect(self.get_view().sort_table_rows)
        self.thread.when_finished.connect(lambda: self.get_view().set_applied_filter_message(True))
        self.thread.when_finished.connect(lambda: self.get_view().set_status_bar_message(''))
        self.thread.when_finished.connect(lambda: self.get_view().disable_all_gui(False))
        self.thread.when_finished.connect(lambda: self.get_view().set_delete_filter_disabled(False))
        self.thread.when_finished.connect(lambda: self.get_view().show_info_toast_message('Filtro aplicado'))


        self.thread.start()

    def __filter_expenses(self, thread: PresenterThreadWorker):
        self.__expenses = self.__expense_repo.get_expenses_by_filter(self.__expense_filter)

    def execute_thread_to_delete_applied_filter(self):
        self.__expense_filter = None
        self.thread = PresenterThreadWorker(self.__load_expenses)

        self.thread.when_started.connect(lambda: self.get_view().set_status_bar_message('Cargando Datos'))
        self.thread.when_started.connect(lambda: self.get_view().disable_all_gui(True))

        self.thread.when_finished.connect(self.get_view().clean_table)
        self.thread.when_finished.connect(self.__fill_table)
        self.thread.when_finished.connect(self.get_view().sort_table_rows)
        self.thread.when_finished.connect(lambda: self.get_view().set_applied_filter_message(False))
        self.thread.when_finished.connect(lambda: self.get_view().set_status_bar_message(''))
        self.thread.when_finished.connect(lambda: self.get_view().disable_all_gui(False))
        self.thread.when_finished.connect(lambda: self.get_view().set_delete_filter_disabled(True))
        self.thread.when_finished.connect(lambda: self.get_view().show_info_toast_message('Filtro quitado'))

        self.thread.start()

