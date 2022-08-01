from easy_mvp.abstract_presenter import AbstractPresenter

from view.week_report import WeekSaleReportView


class WeekSaleReportPresenter(AbstractPresenter):

    def _on_initialize(self):
        self._set_view(WeekSaleReportView(self))

    def close_presenter(self):
        self._close_this_presenter()
