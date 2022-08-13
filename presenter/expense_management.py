from easy_mvp.abstract_presenter import AbstractPresenter
from view.expense_management import ExpenseManagementView


class ExpenseManagementPresenter(AbstractPresenter):

    def _on_initialize(self):
        self._set_view(ExpenseManagementView(self))

    def close_presenter(self):
        self._close_this_presenter()
