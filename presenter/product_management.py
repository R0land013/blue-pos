from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent
from model.entity.models import Product
from model.repository.factory import RepositoryFactory
from model.repository.product import ProductFilter
from presenter.product_presenter import ProductPresenter
from presenter.product_sale_management import ProductSaleManagementPresenter
from presenter.util.thread_worker import PresenterThreadWorker
from view.product_management import ProductManagementView


class ProductManagementPresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__initialize_view()
        self.__product_repo = RepositoryFactory.get_product_repository()
        self.__products = None

    def __initialize_view(self):
        view = ProductManagementView(self)
        self._set_view(view)

    def return_to_main(self):
        self._close_this_presenter()

    def on_view_shown(self):
        self.__execute_thread_to_fill_table()

    def __execute_thread_to_fill_table(self):
        self.thread = PresenterThreadWorker(self.__load_products)
        self.thread.when_started.connect(self.__disable_gui_and_show_loading_products_message)
        self.thread.when_finished.connect(self.__fill_table)
        self.thread.when_finished.connect(self.__set_available_gui_and_show_no_message)
        self.thread.start()

    def __load_products(self, thread: PresenterThreadWorker):
        self.__products = self.__product_repo.get_all_products()

    def __fill_table(self):
        self.get_view().clean_table()
        for a_product in self.__products:
            self.__add_product_to_table(a_product)
        self.get_view().resize_table_columns_to_contents()

    def __disable_gui_and_show_loading_products_message(self):
        self.__set_state_bar_message('Cargando datos...')
        self.__set_disabled_view_except_state_bar(True)

    def __set_state_bar_message(self, message: str):
        self.get_view().set_state_bar_message(message)

    def __set_disabled_view_except_state_bar(self, disabled: bool):
        self.get_view().set_disabled_view_except_status_bar(disabled)

    def __add_product_to_table(self, product: Product):
        self.get_view().add_empty_row_at_the_end_of_table()
        row = self.get_view().get_last_row_index()
        self.__set_table_row_by_product(row, product)

    def __set_table_row_by_product(self, row: int, product: Product):
        view = self.get_view()
        view.set_cell_in_table(row, ProductManagementView.ID_COLUMN, product.id)
        view.set_cell_in_table(row, ProductManagementView.NAME_COLUMN, product.name)
        view.set_cell_in_table(row, ProductManagementView.PRICE_COLUMN, product.price)
        view.set_cell_in_table(row, ProductManagementView.PROFIT_COLUMN, product.profit)
        view.set_cell_in_table(row, ProductManagementView.QUANTITY_COLUMN, product.quantity)

    def __set_available_gui_and_show_no_message(self):
        self.__set_disabled_view_except_state_bar(False)
        self.__set_state_bar_message('')

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
        if self.get_view().ask_user_to_confirm_product_deletion():
            self.__selected_product_id_list = self.get_view().get_all_selected_product_ids()
            self.thread = PresenterThreadWorker(self.__product_deletion)
            self.thread.when_started.connect(self.__disable_gui_and_show_deleting_products_message)
            self.thread.when_finished.connect(self.get_view().delete_selected_products_from_table)
            self.thread.when_finished.connect(self.__set_available_gui_and_show_no_message)
            self.thread.start()

    def __product_deletion(self, thread: PresenterThreadWorker):
        self.__product_repo.delete_products(self.__selected_product_id_list)

    def __disable_gui_and_show_deleting_products_message(self):
        self.__set_state_bar_message('Eliminando productos...')
        self.__set_disabled_view_except_state_bar(True)

    def __get_selected_product(self):
        product_id = self.get_view().get_selected_product_id()
        a_filter = ProductFilter()
        a_filter.id = product_id
        products = self.__product_repo.get_products_by_filter(a_filter)
        if len(products) == 1:
            return products[0]
        return None

    def __get_all_selected_products(self) -> list:
        products = []
        product_id_list = self.get_view().get_all_selected_product_ids()
        a_filter = ProductFilter()
        for product_id in product_id_list:
            a_filter.id = product_id
            a_product = self.__product_repo.get_products_by_filter(a_filter)[0]
            products.append(a_product)
        return products

    def on_view_discovered_with_result(self, action: str, result_data: dict, result: str):
        if result == ProductPresenter.NEW_PRODUCT_RESULT:
            self.__add_new_product_to_table(result_data)
        if result == ProductPresenter.UPDATED_PRODUCT_RESULT:
            self.__update_product_on_table(result_data)
        if result == ProductSaleManagementPresenter.MANAGED_SALES_RESULT:
            self.__update_product_quantity_on_table(result_data)

    def __add_new_product_to_table(self, result_data: dict):
        new_product = result_data[ProductPresenter.NEW_PRODUCT]
        self.__add_product_to_table(new_product)
        self.get_view().resize_table_columns_to_contents()

    def __update_product_on_table(self, result_data: dict):
        updated_product = result_data[ProductPresenter.UPDATED_PRODUCT]
        row = self.get_view().get_selected_row_index()
        self.__set_table_row_by_product(row, updated_product)

    def __update_product_quantity_on_table(self, result_data: dict):
        new_product_quantity = result_data[ProductSaleManagementPresenter.REMAINING_PRODUCT_QUANTITY]
        row = self.get_view().get_selected_row_index()
        self.get_view().set_cell_in_table(row, ProductManagementView.QUANTITY_COLUMN, new_product_quantity)

    def open_product_sale_management_presenter(self):
        selected_product = self.__get_selected_product()
        data = {ProductSaleManagementPresenter.PRODUCT_DATA: selected_product}

        intent = Intent(ProductSaleManagementPresenter)
        intent.set_data(data)
        self._open_other_presenter(intent)
