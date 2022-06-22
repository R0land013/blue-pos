from PyQt5.QtCore import pyqtSignal
from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent

from model.repository.factory import RepositoryFactory
from model.repository.product import ProductFilter
from presenter.product_presenter import ProductPresenter
from presenter.util.thread_worker import PresenterThreadWorker
from view.product_management import ProductManagementView


class ProductManagementPresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__initialize_view()
        self.__product_repo = RepositoryFactory.get_product_repository()

    def __initialize_view(self):
        view = ProductManagementView(self)
        self._set_view(view)

    def return_to_main(self):
        self._close_this_presenter()

    def on_view_shown(self):
        self.__execute_thread_to_fill_table()

    def __execute_thread_to_fill_table(self):
        self.thread = PresenterThreadWorker(self.fill_table)
        self.thread.start()

    def fill_table(self, error_found: pyqtSignal, finished_without_error: pyqtSignal):
        self.get_view().clean_table()
        self.__set_state_bar_message('Cargando datos...')
        self.__set_disabled_view_except_state_bar(True)

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

        self.__set_disabled_view_except_state_bar(False)
        self.__set_state_bar_message('Datos cargados')

    def __set_state_bar_message(self, message: str):
        self.get_view().set_state_bar_message(message)

    def __set_disabled_view_except_state_bar(self, disabled: bool):
        self.get_view().set_disabled_view_except_status_bar(disabled)

    def open_presenter_to_create_new_product(self):
        intent = Intent(ProductPresenter)
        intent.set_action(ProductPresenter.NEW_PRODUCT_ACTION)
        intent.use_new_window(True)
        intent.use_modal(True)

        self._open_other_presenter(intent)

    def open_presenter_to_edit_product(self):
        product_id = self.get_view().get_selected_product_id()
        data = {ProductPresenter.PRODUCT_ID: product_id}

        intent = Intent(ProductPresenter)
        intent.set_action(ProductPresenter.EDIT_PRODUCT_ACTION)
        intent.use_new_window()
        intent.use_modal(True)
        intent.set_data(data)

        self._open_other_presenter(intent)

    def delete_selected_product(self):
        product_id = self.get_view().get_selected_product_id()
        a_filter = ProductFilter()
        a_filter.id = product_id
        product = self.__product_repo.get_products_by_filter(a_filter)[0]
        self.__product_repo.delete_product(product)

    def on_view_discovered_with_result(self, action: str, result_data: dict, result: str):
        if result == ProductPresenter.NEW_PRODUCT_RESULT:
            self.__execute_thread_to_fill_table()
