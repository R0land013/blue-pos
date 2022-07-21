from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent

from model.entity.models import Sale
from model.repository.factory import RepositoryFactory
from model.repository.sale import SaleFilter
from presenter.edit_sale import EditSalePresenter
from presenter.sale_filter import SaleFilterPresenter
from presenter.sell_product import MakeSalePresenter
from presenter.util.thread_worker import PresenterThreadWorker
from view.product_sale_management import ProductSaleManagementView


class ProductSaleManagementPresenter(AbstractPresenter):

    PRODUCT_DATA = 'product'

    def _on_initialize(self):
        view = ProductSaleManagementView(self)
        self._set_view(view)
        self.__product = self._get_intent_data()[self.PRODUCT_DATA]
        self.__sale_repo = RepositoryFactory.get_sale_repository()
        self.__applied_sale_filter = None

    def close_presenter(self):
        self._close_this_presenter()

    def open_filter_presenter(self):
        intent = Intent(SaleFilterPresenter)
        data = {SaleFilterPresenter.FILTER_BY_PRODUCT_ID_LIST_DATA: [self.__product.id]}
        intent.set_data(data)

        intent.use_new_window(True)
        intent.use_modal(True)
        self._open_other_presenter(intent)

    def on_view_shown(self):
        self.get_view().set_available_product_quantity(self.__product.quantity)
        self.__set_sell_button_availability_depending_on_remaining_product_quantity()
        self.__execute_thread_to_fill_table()

    def __set_sell_button_availability_depending_on_remaining_product_quantity(self):
        if self.__product.quantity == 0:
            self.get_view().disable_sell_button(True)
        else:
            self.get_view().disable_sell_button(False)

    def __execute_thread_to_fill_table(self):
        self.thread = PresenterThreadWorker(self.fill_table)
        self.thread.finished_without_error.connect(self.__on_successful_loaded_data)
        self.thread.start()

    def fill_table(self, thread: PresenterThreadWorker = None):
        self.get_view().set_disabled_view_except_status_bar(True)
        self.get_view().set_status_bar_message('Cargando datos...')
        self.get_view().clean_table()

        product_sales = self.__get_sales_of_product()
        for a_sale in product_sales:
            self.__add_sale_to_table(a_sale)

        thread.finished_without_error.emit()

    def __get_sales_of_product(self):
        filter_by_product_id = SaleFilter()
        filter_by_product_id.product_id_list = [self.__product.id]

        return self.__sale_repo.get_sales_by_filter(filter_by_product_id)

    def __add_sale_to_table(self, sale: Sale):
        self.get_view().add_empty_row_at_the_end_of_table()
        row = self.get_view().get_last_row_index()
        self.__set_table_row_by_sale(row, sale)

    def __set_table_row_by_sale(self, row: int, sale: Sale):
        view = self.get_view()
        view.set_cell_in_table(row, ProductSaleManagementView.SALE_ID_COLUMN, sale.id)
        view.set_cell_in_table(row, ProductSaleManagementView.PAYMENT_COLUMN, sale.price)
        view.set_cell_in_table(row, ProductSaleManagementView.PROFIT_COLUMN, sale.profit)
        view.set_cell_in_table(row, ProductSaleManagementView.SALE_DATE_COLUMN, sale.date)

    def __on_successful_loaded_data(self):
        self.get_view().resize_table_columns_to_contents()
        self.get_view().set_disabled_view_except_status_bar(False)
        self.get_view().set_status_bar_message('')

    def undo_selected_sales(self):
        if self.get_view().ask_user_to_confirm_undo_sales():
            self.thread = PresenterThreadWorker(self.__undo_selected_sales)
            self.thread.when_finished.connect(self.get_view().delete_selected_sales_from_table)
            self.thread.when_finished.connect(
                self.__set_sell_button_availability_depending_on_remaining_product_quantity)
            self.thread.start()

    def __update_available_product_quantity_on_gui(self):
        # Aquí no es necesario realizar ninguna substracción porque SqlAlchemy
        # se encarga de actualizar el valor de los atributos cada vez que son accedidos
        self.get_view().set_available_product_quantity(self.__product.quantity)

    def __undo_selected_sales(self, thread: PresenterThreadWorker = None):
        self.get_view().set_disabled_view_except_status_bar(True)
        self.get_view().set_status_bar_message('Procesando...')

        sale_id_list = self.get_view().get_selected_sale_ids()
        self.__sale_repo.delete_sales(sale_id_list)

        self.__update_available_product_quantity_on_gui()
        self.get_view().set_disabled_view_except_status_bar(False)
        self.get_view().set_status_bar_message('')

    def __construct_mock_sales_to_execute_deletion(self):
        sale_ids = self.get_view().get_selected_sale_ids()
        mock_sales = []
        for an_id in sale_ids:
            mock_sales.append(Sale(id=an_id, product_id=self.__product.id))
        return mock_sales

    def open_make_sale_presenter(self):
        data = {MakeSalePresenter.PRODUCT: self.__product}
        intent = Intent(MakeSalePresenter)
        intent.set_data(data)
        intent.use_new_window(True)
        intent.use_modal(True)
        self._open_other_presenter(intent)

    def on_view_discovered_with_result(self, action: str, result_data: dict, result: str):
        if result == MakeSalePresenter.NEW_SALES_RESULT:
            self.__update_gui_on_new_sales_inserted(result_data)

        elif result == EditSalePresenter.UPDATED_SALE_RESULT:
            self.__update_sale_on_table(result_data)

        elif result == SaleFilterPresenter.NEW_FILTER_RESULT:
            self.__execute_thread_to_apply_sale_filter(result_data)

    def __update_gui_on_new_sales_inserted(self, result_data: dict):
        new_sales = result_data[MakeSalePresenter.NEW_SALES]
        for a_sale in new_sales:
            self.__add_sale_to_table(a_sale)
        self.__update_available_product_quantity_on_gui()
        self.__set_sell_button_availability_depending_on_remaining_product_quantity()

    def __update_sale_on_table(self, result_data: dict):
        selected_row = self.get_view().get_selected_row_index()
        updated_sale = result_data[EditSalePresenter.UPDATED_SALE]
        self.__set_table_row_by_sale(selected_row, updated_sale)

    def open_presenter_to_edit_sale(self):
        data = {EditSalePresenter.SALE: self.__get_selected_sale()}
        intent = Intent(EditSalePresenter)
        intent.use_new_window(True)
        intent.use_modal(True)
        intent.set_data(data)
        self._open_other_presenter(intent)

    def __get_selected_sale(self) -> Sale:
        sale_id = self.get_view().get_selected_sale_ids()[0]
        filter_by_id = SaleFilter()
        filter_by_id.sale_id_list = [sale_id]
        return self.__sale_repo.get_sales_by_filter(filter_by_id)[0]

    def __execute_thread_to_apply_sale_filter(self, result_data: dict):
        self.__applied_sale_filter = result_data[SaleFilterPresenter.NEW_FILTER_DATA]
        self.thread = PresenterThreadWorker(self.__fill_table_using_filter)
        self.thread.when_started.connect(self.__show_message_to_demonstrate_the_filtering_is_running)
        self.thread.finished_without_error.connect(self.__show_filtered_sales_message)
        self.thread.start()

    def __fill_table_using_filter(self, thread: PresenterThreadWorker):

        self.get_view().clean_table()
        filtered_sales = self.__sale_repo.get_sales_by_filter(self.__applied_sale_filter)
        for a_sale in filtered_sales:
            self.__add_sale_to_table(a_sale)

        thread.finished_without_error.emit()

    def __show_message_to_demonstrate_the_filtering_is_running(self):
        self.get_view().set_disabled_view_except_status_bar(True)
        self.get_view().set_status_bar_message('Filtrando ventas...')

    def __show_filtered_sales_message(self):
        self.get_view().set_disabled_view_except_status_bar(False)
        self.get_view().set_filter_applied_message(True)
        self.get_view().set_status_bar_message('')
