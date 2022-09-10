from datetime import date, timedelta
from typing import Tuple

from easy_mvp.abstract_presenter import AbstractPresenter

from model.entity.economic_summary import EconomicSummary
from model.repository.factory import RepositoryFactory
from presenter.util.thread_worker import PresenterThreadWorker
from view.month_statistics import MonthStatisticsView


class MonthStatisticsPresenter(AbstractPresenter):

    def _on_initialize(self):
        self._set_view(MonthStatisticsView(self))
        self.__selected_month_date: date = None
        self.__summary_repo = RepositoryFactory.get_economic_summary_repository()
        self.__day_summaries: Tuple[EconomicSummary] = None

    def close_presenter(self):
        self._close_this_presenter()

    def get_default_window_title(self) -> str:
        return 'Blue POS - Estadísticas Mensuales'

    def calculate_economic_day_summaries(self):
        self.__selected_month_date = self.get_view().get_selected_month_date()
        self.thread = PresenterThreadWorker(self.__load_day_summaries)

        self.thread.when_started.connect(lambda: self.get_view().disable_gui(True))
        self.thread.when_started.connect(lambda: self.get_view().set_status_bar_message('Calculando...'))

        self.thread.when_finished.connect(self.__plot_summaries_on_graph)
        self.thread.when_started.connect(lambda: self.get_view().disable_gui(False))
        self.thread.when_started.connect(lambda: self.get_view().set_status_bar_message(''))

        self.thread.start()

    def __load_day_summaries(self, thread: PresenterThreadWorker):
        current_date = date(day=1, month=self.__selected_month_date.month, year=self.__selected_month_date.year)
        summaries_list = []

        while current_date.month == self.__selected_month_date.month and current_date <= date.today():

            summaries_list.append(self.__summary_repo.get_economic_summary_on_day(current_date))
            current_date = current_date + timedelta(days=1)

        self.__day_summaries = tuple(summaries_list)

    def __plot_summaries_on_graph(self):
        days = list(map(lambda summary: summary.initial_date.day, self.__day_summaries))
        net_profit_values = list(map(lambda summary: float(summary.net_profit.amount), self.__day_summaries))

        self.get_view().plot_values(x_days_values=days, y_values=net_profit_values)
