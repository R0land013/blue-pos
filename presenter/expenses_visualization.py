from easy_mvp.abstract_presenter import AbstractPresenter

from model.entity.models import Expense
from view.expenses_visualization import ExpensesVisualizationView


class ExpensesVisualizationPresenter(AbstractPresenter):

    INITIAL_DATE_DATA = 'initial_date_data'
    FINAL_DATE_DATA = 'final_date_data'
    TOTAL_EXPENSE_DATA = 'total_expense_data'
    EXPENSES_DATA = 'expenses_data'

    def _on_initialize(self):
        self._set_view(ExpensesVisualizationView(self))
        self.__initial_date = self._get_intent_data()[self.INITIAL_DATE_DATA]
        self.__final_date = self._get_intent_data()[self.FINAL_DATE_DATA]
        self.__total_expense = self._get_intent_data()[self.TOTAL_EXPENSE_DATA]
        self.__expenses = self._get_intent_data()[self.EXPENSES_DATA]

    def on_view_shown(self):
        self.get_view().disable_view(True)
        self.get_view().set_status_bar_message('Cargando gastos...')

        self.get_view().set_date_range_for_message(self.__initial_date, self.__final_date)
        self.get_view().set_total_expense(self.__total_expense)
        self.__fill_table()
        self.get_view().set_first_row_selected()

        self.get_view().disable_view(False)
        self.get_view().set_status_bar_message('')

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
        view.set_cell_in_table(row, ExpensesVisualizationView.ID_COLUMN, an_expense.id)
        view.set_cell_in_table(row, ExpensesVisualizationView.NAME_COLUMN, an_expense.name)
        view.set_cell_in_table(row, ExpensesVisualizationView.SPENT_MONEY_COLUMN, an_expense.spent_money)
        view.set_cell_in_table(row, ExpensesVisualizationView.DATE_COLUMN, an_expense.date)

    def close_presenter(self):
        self._close_this_presenter()

    def get_default_window_title(self) -> str:
        return 'Gastos'

    def set_expense_description(self):
        selected_id = self.get_view().get_selected_expense_id()
        selected_expense = list(filter(lambda exp: exp.id == selected_id, self.__expenses))[0]
        self.get_view().set_description(selected_expense.description)
