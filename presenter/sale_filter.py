from easy_mvp.abstract_presenter import AbstractPresenter

from view.sale_filter import SaleFilterView


class SaleFilterPresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__initialize_view()

    def __initialize_view(self):
        self._set_view(SaleFilterView(self))

    def close_presenter(self):
        self._close_this_presenter()