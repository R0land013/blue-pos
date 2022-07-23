from easy_mvp.abstract_presenter import AbstractPresenter
from view.day_report import DaySaleReportView


class DaySaleReportPresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__initialize_view()

    def __initialize_view(self):
        view = DaySaleReportView(self)
        self._set_view(view)

    def close_presenter(self):
        self._close_this_presenter()
