from easy_mvp.abstract_presenter import AbstractPresenter
from view.edit_sale import EditSaleView


class EditSalePresenter(AbstractPresenter):

    SALE = 'sale'

    def _on_initialize(self):
        self.__initialize_view()

    def __initialize_view(self):
        view = EditSaleView(self)
        self._set_view(view)
