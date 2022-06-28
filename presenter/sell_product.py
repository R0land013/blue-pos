from easy_mvp.abstract_presenter import AbstractPresenter
from view.sell_product import MakeSaleView


class MakeSalePresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__initialize_view()

    def __initialize_view(self):
        view = MakeSaleView(self)
        self._set_view(view)
