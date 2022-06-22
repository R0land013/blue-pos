from PyQt5.QtCore import pyqtSignal
from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent
from model.entity.models import Product
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

        for a_product in products:
            self.__add_product_to_table(a_product)

        view.resize_table_columns_to_contents()

        self.__set_disabled_view_except_state_bar(False)
        self.__set_state_bar_message('Datos cargados')

    def __set_state_bar_message(self, message: str):
        self.get_view().set_state_bar_message(message)

    def __set_disabled_view_except_state_bar(self, disabled: bool):
        self.get_view().set_disabled_view_except_status_bar(disabled)

    def __add_product_to_table(self, product: Product):
        view = self.get_view()
        view.add_empty_row_at_the_end_of_table()
        row = view.get_last_row_index()

        view.set_cell_in_table(row, ProductManagementView.ID_COLUMN, product.id)
        view.set_cell_in_table(row, ProductManagementView.NAME_COLUMN, product.name)
        view.set_cell_in_table(row, ProductManagementView.DESCRIPTION_COLUMN, product.description)
        view.set_cell_in_table(row, ProductManagementView.PRICE_COLUMN, product.price)
        view.set_cell_in_table(row, ProductManagementView.PROFIT_COLUMN, product.profit)
        view.set_cell_in_table(row, ProductManagementView.QUANTITY_COLUMN, product.quantity)

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
        intent.use_new_window(True)
        intent.use_modal(True)
        intent.set_data(data)

        self._open_other_presenter(intent)

    def delete_selected_product(self):
        self.thread = PresenterThreadWorker(self.__product_deletion)
        self.thread.start()

    def __product_deletion(self, error_found: pyqtSignal, finished_without_error: pyqtSignal):
        self.__set_state_bar_message('Procesando...')
        self.__set_disabled_view_except_state_bar(True)

        product = self.__get_selected_product()
        self.__product_repo.delete_product(product)

        self.get_view().delete_selected_product_from_table()
        self.__set_state_bar_message('Producto eliminado')
        self.__set_disabled_view_except_state_bar(False)

    def __get_selected_product(self):
        product_id = self.get_view().get_selected_product_id()
        a_filter = ProductFilter()
        a_filter.id = product_id
        products = self.__product_repo.get_products_by_filter(a_filter)
        if len(products) == 1:
            return products[0]
        return None

    def on_view_discovered_with_result(self, action: str, result_data: dict, result: str):
        if result == ProductPresenter.NEW_PRODUCT_RESULT:
            self.__add_new_product_to_table(result_data)
        if result in (ProductPresenter.UPDATED_PRODUCT_RESULT,):
            self.__execute_thread_to_fill_table()

    def __add_new_product_to_table(self, result_data: dict):
        new_product = result_data[ProductPresenter.NEW_PRODUCT]
        self.__add_product_to_table(new_product)