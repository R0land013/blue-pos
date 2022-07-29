from easy_mvp.abstract_presenter import AbstractPresenter

from view.month_report import MonthSaleReportView


class MonthSaleReportPresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__initialize_view()

    def __initialize_view(self):
        self._set_view(MonthSaleReportView(self))

    def close_presenter(self):
        self._close_this_presenter()