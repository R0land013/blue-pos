from easy_mvp.abstract_presenter import AbstractPresenter

from view.expense_form import ExpenseFormView


class ExpenseFormPresenter(AbstractPresenter):

    def _on_initialize(self):
        self._set_view(ExpenseFormView(self))

    def close_presenter(self):
        self._close_this_presenter()
