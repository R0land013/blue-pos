from easy_mvp.abstract_presenter import AbstractPresenter

from view.custom_report import CustomSaleReportView


class CustomSaleReportPresenter(AbstractPresenter):

    def _on_initialize(self):
        self._set_view(CustomSaleReportView(self))

    def close_presenter(self):
        self._close_this_presenter()
