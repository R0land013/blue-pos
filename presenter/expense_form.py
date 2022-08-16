from easy_mvp.abstract_presenter import AbstractPresenter

from model.entity.models import Expense
from model.repository.exc.expense import EmptyExpenseNameException
from model.repository.factory import RepositoryFactory
from model.util.monetary_types import CUPMoney
from presenter.util.thread_worker import PresenterThreadWorker
from view.expense_form import ExpenseFormView


class ExpenseFormPresenter(AbstractPresenter):

    CREATE_NEW_EXPENSE_ACTION = 'create_new_expense_action'

    NEW_EXPENSE_CREATED_RESULT = 'new_expense_created_result'

    NEW_EXPENSE_RESULT_DATA = 'new_expense_data'

    def _on_initialize(self):
        self._set_view(ExpenseFormView(self))
        self.__expense_repo = RepositoryFactory.get_expense_repository()
        self.__constructed_expense = None

    def close_presenter(self):
        self._close_this_presenter()

    def get_default_window_title(self) -> str:
        return 'Blue POS - Nuevo gasto'

    def on_view_shown(self):
        if self._get_intent_action() == self.CREATE_NEW_EXPENSE_ACTION:
            self.get_view().hide_id_labels(True)
        self.get_view().set_status_bar_message('')

    def execute_thread_to_save_expense(self):
        self.__construct_expense_from_gui_fields()
        self.thread = PresenterThreadWorker(self.insert_expense)
        self.thread.when_started.connect(self.__disable_all_view_and_show_processing_message)

        self.thread.error_found.connect(self.__handle_errors)
        self.thread.finished_without_error.connect(
            self.__close_this_presenter_and_notify_new_expense_created)

        self.thread.start()

    def __construct_expense_from_gui_fields(self):
        self.__constructed_expense = Expense()
        view = self.get_view()
        self.__constructed_expense.name = view.get_expense_name()
        self.__constructed_expense.description = view.get_expense_description()
        self.__constructed_expense.spent_money = CUPMoney(view.get_spent_money())
        self.__constructed_expense.date = view.get_date()

    def insert_expense(self, thread: PresenterThreadWorker):
        try:
            self.__expense_repo.insert_expense(self.__constructed_expense)
            thread.finished_without_error.emit()
        except EmptyExpenseNameException as e:
            thread.error_found.emit(e)

    def __disable_all_view_and_show_processing_message(self):
        self.get_view().disable_all_gui(True)
        self.get_view().set_status_bar_message('Procesando...')

    def __handle_errors(self, exception):
        if isinstance(exception, EmptyExpenseNameException):
            self.get_view().show_dialog_error_message('El nombre no puede estar vacío.')
            self.get_view().disable_all_gui(False)
            self.get_view().set_status_bar_message('')

    def __close_this_presenter_and_notify_new_expense_created(self):
        result_data = {self.NEW_EXPENSE_RESULT_DATA: self.__constructed_expense}
        self._close_this_presenter_with_result(result_data, self.NEW_EXPENSE_CREATED_RESULT)