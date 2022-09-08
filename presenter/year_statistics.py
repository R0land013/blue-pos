from datetime import date
from typing import Tuple
from easy_mvp.abstract_presenter import AbstractPresenter

from model.entity.economic_summary import EconomicSummary
from model.repository.factory import RepositoryFactory
from presenter.util.thread_worker import PresenterThreadWorker
from view.year_statistics import YearStatisticsView


class YearStatisticsPresenter(AbstractPresenter):

    def _on_initialize(self):
        self._set_view(YearStatisticsView(self))
        self.__summary_repo = RepositoryFactory.get_economic_summary_repository()
        self.__selected_year: int = 2000
        self.__month_summaries: Tuple[EconomicSummary] = None

    def close_presenter(self):
        self._close_this_presenter()

    def get_default_window_title(self) -> str:
        return 'Blue POS - Estadísticas Anuales'

    def calculate_economic_month_summaries(self):
        self.__selected_year = self.get_view().get_selected_year()
        self.thread = PresenterThreadWorker(self.__load_summaries)

        self.thread.when_started.connect(lambda: self.get_view().disable_gui(True))
        self.thread.when_started.connect(lambda: self.get_view().set_status_bar_message('Calculando...'))

        self.thread.when_finished.connect(self.__plot_summaries_on_graph)
        self.thread.when_finished.connect(lambda: self.get_view().disable_gui(False))
        self.thread.when_started.connect(lambda: self.get_view().set_status_bar_message(''))

        self.thread.start()

    def __load_summaries(self, thread: PresenterThreadWorker):
        summaries_list = []
        current_month = 1
        while current_month <= 12:
            month_date = date(day=1, month=current_month, year=self.__selected_year)
            summaries_list.append(self.__summary_repo.get_economic_summary_on_month(month_date))

            current_month += 1
        self.__month_summaries = tuple(summaries_list)

    def __plot_summaries_on_graph(self):
        months_values = list(map(lambda summary: summary.initial_date.month, self.__month_summaries))
        net_profit_values = list(map(lambda summary: float(summary.net_profit.amount), self.__month_summaries))

        self.get_view().plot_values(month_axis=months_values, y_axis=net_profit_values)

    def change_vertical_axis(self, selected_axis_option: str):
        month_values = list(map(lambda summary: summary.initial_date.month, self.__month_summaries))
        new_y_axis = None

        if selected_axis_option == YearStatisticsView.NET_PROFIT_ITEM:
            new_y_axis = list(map(lambda summary: float(summary.net_profit.amount), self.__month_summaries))
        elif selected_axis_option == YearStatisticsView.SALE_QUANTITY_ITEM:
            new_y_axis = list(map(lambda summary: summary.sale_quantity, self.__month_summaries))
        elif selected_axis_option == YearStatisticsView.TOTAL_EXPENSE_ITEM:
            new_y_axis = list(map(lambda summary: float(summary.total_expense.amount), self.__month_summaries))

        self.get_view().plot_values(month_axis=month_values, y_axis=new_y_axis)

    def create_tool_tip_for_spot(self, x: float, y: float, data):
        x_month = int(x)
        hovered_summary: EconomicSummary = list(filter(
            lambda summary: summary.initial_date.month == x_month,
            self.__month_summaries))[0]

        return f'Cantidad de ventas: {hovered_summary.sale_quantity}\n\n' \
               f'Dinero obtenido:    {hovered_summary.acquired_money.amount} CUP\n' \
               f'Costos totales:    -{hovered_summary.total_cost.amount} CUP\n' \
               f'Ganacias totales:   {hovered_summary.total_profit.amount} CUP\n' \
               f'Gastos totales:    -{hovered_summary.total_expense.amount} CUP\n\n' \
               f'Ganancia neta:      {hovered_summary.net_profit.amount} CUP'
