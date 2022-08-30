from easy_mvp.abstract_presenter import AbstractPresenter

from view.expenses_visualization import ExpensesVisualizationView


class ExpensesVisualizationPresenter(AbstractPresenter):

    def _on_initialize(self):
        self._set_view(ExpensesVisualizationView(self))

    def close_presenter(self):
        self._close_this_presenter()

    def get_default_window_title(self) -> str:
        return 'Gastos'