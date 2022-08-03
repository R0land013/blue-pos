from easy_mvp.abstract_presenter import AbstractPresenter
from view.product_selection import ProductSelectionView


class ProductSelectionPresenter(AbstractPresenter):

    def _on_initialize(self):
        self._set_view(ProductSelectionView(self))

    def cancel_selection_and_close_presenter(self):
        self._close_this_presenter()
