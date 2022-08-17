from easy_mvp.abstract_presenter import AbstractPresenter

from view.expense_filter import ExpenseFilterView


class ExpenseFilterPresenter(AbstractPresenter):

    def get_default_window_title(self) -> str:
        return 'Filtrar gastos'

    def _on_initialize(self):
        self._set_view(ExpenseFilterView(self))

    def close_presenter(self):
        self._close_this_presenter()