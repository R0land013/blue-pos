from easy_mvp.abstract_presenter import AbstractPresenter
from view.product_sale_management import ProductSaleManagementView


class ProductSaleManagementPresenter(AbstractPresenter):

    def _on_initialize(self):
        view = ProductSaleManagementView(self)
        self._set_view(view)

    def close_presenter(self):
        self._close_this_presenter()
