from easy_mvp.abstract_presenter import AbstractPresenter

from view.year_report import YearSaleReportView


class YearSaleReportPresenter(AbstractPresenter):

    def _on_initialize(self):
        self._set_view(YearSaleReportView(self))

    def close_presenter(self):
        self._close_this_presenter()