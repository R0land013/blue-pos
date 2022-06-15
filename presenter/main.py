from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent
from presenter.product_management import ProductManagementPresenter
from view.main import MainView


class MainPresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__initialize_view()

    def __initialize_view(self):
        view = MainView(self)
        self._set_view(view)

    def open_product_management(self):
        intent = Intent(ProductManagementPresenter)
        self._open_other_presenter(intent)
