from easy_mvp.abstract_presenter import AbstractPresenter

from view.year_statistics import YearStatisticsView


class YearStatisticsPresenter(AbstractPresenter):

    def _on_initialize(self):
        self._set_view(YearStatisticsView(self))

    def close_presenter(self):
        self._close_this_presenter()

    def get_default_window_title(self) -> str:
        return 'Blue POS - Estadísticas Anuales'