from easy_mvp.abstract_presenter import AbstractPresenter

from model.entity.models import Product
from model.repository.factory import RepositoryFactory
from presenter.util.thread_worker import PresenterThreadWorker
from view.product_selection import ProductSelectionView


class ProductSelectionPresenter(AbstractPresenter):

    NEW_SELECTED_PRODUCTS_RESULT = 'new_selected_products_result'

    SELECTED_PRODUCTS_DATA = 'selected_products_data'
    NEW_SELECTED_PRODUCTS_DATA = 'new_selected_products'

    def _on_initialize(self):
        self._set_view(ProductSelectionView(self))
        self.__product_repo = RepositoryFactory.get_product_repository()

        # se usa list() para crear una nuevo objeto con las mismas referencias
        # que se pasaron a través de SELECTED_PRODUCTS_DATA. Esto se hace para
        # no modificar la lista que se pasó a este presentador y tener una disponible
        # que sea modificable
        self.__selected_products = list(self._get_intent_data()[self.SELECTED_PRODUCTS_DATA])
        self.__remaining_products = []

    def cancel_selection_and_close_presenter(self):
        self._close_this_presenter()

    def on_view_shown(self):
        self.__execute_thread_to_load_products()

    def __execute_thread_to_load_products(self):
        self.thread = PresenterThreadWorker(self.__load_remaining_products)

        self.thread.when_started.connect(self.__disable_gui_and_show_loading_products_message)

        self.thread.when_finished.connect(self.__fill_selected_product_table)
        self.thread.when_finished.connect(self.__fill_remaining_product_table)
        self.thread.when_finished.connect(self.__set_gui_available_and_hide_state_bar)
        self.thread.when_finished.connect(
            self.__disable_take_all_and_empty_buttons_depending_on_product_quantities)
        self.thread.start()

    def __load_remaining_products(self, thread: PresenterThreadWorker):
        products = self.__product_repo.get_all_products()
        self.__remaining_products = list(filter(lambda a_product: a_product not in self.__selected_products,
                                                products))

    def __disable_gui_and_show_loading_products_message(self):
        self.get_view().disable_all_gui(True)
        self.get_view().set_state_bar_message('Cargando productos...')

    def __fill_selected_product_table(self):
        self.get_view().clean_selected_product_table()
        for a_product in self.__selected_products:
            self.__add_product_to_selected_product_table(a_product)
        self.get_view().resize_table_columns_to_contents_on_selected_product_table()

    def __add_product_to_selected_product_table(self, a_product: Product):
        view = self.get_view()
        view.add_empty_row_at_the_end_of_selected_product_table()
        row = view.get_last_row_index_from_selected_product_table()
        view.set_cell_in_selected_product_table(row, ProductSelectionView.PRODUCT_ID_COLUMN, a_product.id)
        view.set_cell_in_selected_product_table(row, ProductSelectionView.PRODUCT_NAME_COLUMN, a_product.name)

    def __fill_remaining_product_table(self):
        self.get_view().clean_remaining_product_table()
        for a_product in self.__remaining_products:
            self.__add_product_to_remaining_product_table(a_product)
        self.get_view().resize_table_columns_to_contents_on_remaining_product_table()

    def __add_product_to_remaining_product_table(self, a_product: Product):
        view = self.get_view()
        view.add_empty_row_at_the_end_of_remaining_product_table()
        row = view.get_last_row_index_from_remaining_product_table()
        view.set_cell_in_remaining_product_table(row, ProductSelectionView.PRODUCT_ID_COLUMN, a_product.id)
        view.set_cell_in_remaining_product_table(row, ProductSelectionView.PRODUCT_NAME_COLUMN, a_product.name)

    def __set_gui_available_and_hide_state_bar(self):
        self.get_view().disable_all_gui(False)
        self.get_view().hide_state_bar()

    def __disable_take_all_and_empty_buttons_depending_on_product_quantities(self):
        self.get_view().disable_take_all_button(len(self.__remaining_products) == 0)
        self.get_view().disable_empty_button(len(self.__selected_products) == 0)

    def send_selected_products_to_remaining_table(self):
        self.__send_selected_products_to_remaining_product_list()
        self.__fill_selected_product_table()
        self.__fill_remaining_product_table()
        self.__disable_take_all_and_empty_buttons_depending_on_product_quantities()

    def __send_selected_products_to_remaining_product_list(self):
        selected_product_ids = self.get_view().get_selected_product_ids_from_selected_product_table()
        sending_products = list(filter(lambda a_product: a_product.id in selected_product_ids,
                                       self.__selected_products))
        self.__remaining_products = self.__remaining_products + sending_products
        self.__selected_products = list(filter(lambda a_product: a_product not in sending_products,
                                               self.__selected_products))

    def send_selected_products_to_selected_product_table(self):
        self.__send_selected_products_to_selected_product_list()
        self.__fill_selected_product_table()
        self.__fill_remaining_product_table()
        self.__disable_take_all_and_empty_buttons_depending_on_product_quantities()

    def __send_selected_products_to_selected_product_list(self):
        selected_product_ids = self.get_view().get_selected_product_ids_from_remaining_product_table()
        sending_products = list(filter(lambda a_product: a_product.id in selected_product_ids,
                                       self.__remaining_products))
        self.__selected_products.extend(sending_products)
        self.__remaining_products = list(filter(lambda a_product: a_product not in sending_products,
                                                self.__remaining_products))

    def take_all_remaining_products(self):
        self.__selected_products.extend(self.__remaining_products)
        self.__remaining_products = []
        self.__fill_selected_product_table()
        self.__fill_remaining_product_table()
        self.__disable_take_all_and_empty_buttons_depending_on_product_quantities()

    def empty_selected_products_table(self):
        self.__remaining_products.extend(self.__selected_products)
        self.__selected_products = []
        self.__fill_selected_product_table()
        self.__fill_remaining_product_table()
        self.__disable_take_all_and_empty_buttons_depending_on_product_quantities()

    def close_presenter_and_return_new_selected_products(self):
        result_data = {self.NEW_SELECTED_PRODUCTS_DATA: self.__selected_products}
        self._close_this_presenter_with_result(result=self.NEW_SELECTED_PRODUCTS_RESULT,
                                               result_data=result_data)
