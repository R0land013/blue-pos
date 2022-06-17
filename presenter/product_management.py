from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent

from model.repository.factory import RepositoryFactory
from presenter.product_presenter import ProductPresenter
from view.product_management import ProductManagementView


class ProductManagementPresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__initialize_view()
        self.__product_repo = RepositoryFactory.get_product_repository()
        self.__product_repo.add_on_data_changed_listener(self)

    def __initialize_view(self):
        view = ProductManagementView(self)
        self._set_view(view)

    def return_to_main(self):
        self._close_this_presenter()

    def on_view_shown(self):
        self.__fill_table()

    def __fill_table(self):
        view = self.get_view()
        products = self.__product_repo.get_all_products()

        for index in range(len(products)):
            row = index
            a_product = products[index]
            view.add_empty_row_at_the_end_of_table()

            view.set_cell_in_table(row, ProductManagementView.ID_COLUMN, a_product.id)
            view.set_cell_in_table(row, ProductManagementView.NAME_COLUMN, a_product.name)
            view.set_cell_in_table(row, ProductManagementView.DESCRIPTION_COLUMN, a_product.description)
            view.set_cell_in_table(row, ProductManagementView.PRICE_COLUMN, a_product.price)
            view.set_cell_in_table(row, ProductManagementView.PROFIT_COLUMN, a_product.profit)
            view.set_cell_in_table(row, ProductManagementView.QUANTITY_COLUMN, a_product.quantity)
        view.resize_table_columns_to_contents()

    def open_presenter_to_create_new_product(self):
        intent = Intent(ProductPresenter)
        intent.set_action(ProductPresenter.NEW_PRODUCT_ACTION)
        intent.use_new_window(True)
        intent.use_modal(True)

        self._open_other_presenter(intent)

    def on_data_changed(self):
        self.get_view().clean_table()
        self.__fill_table()
