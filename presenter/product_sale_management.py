from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent

from model.entity.models import Sale, Product
from model.repository.factory import RepositoryFactory
from model.repository.sale import SaleFilter
from presenter.edit_sale import EditSalePresenter
from presenter.sale_filter import SaleFilterPresenter
from presenter.sell_product import MakeSalePresenter
from presenter.util.thread_worker import PresenterThreadWorker
from view.product_sale_management import ProductSaleManagementView


class ProductSaleManagementPresenter(AbstractPresenter):

    MANAGED_SALES_RESULT = 'managed_sales_result'

    PRODUCT_DATA = 'product'

    REMAINING_PRODUCT_QUANTITY = 'remaining_product_quantity'

    def _on_initialize(self):
        view = ProductSaleManagementView(self)
        self._set_view(view)
        self.__product: Product = self._get_intent_data()[self.PRODUCT_DATA]
        self.__sale_repo = RepositoryFactory.get_sale_repository()
        self.__applied_sale_filter: SaleFilter = None

    def close_presenter(self):
        result_data = {self.REMAINING_PRODUCT_QUANTITY: self.__product.quantity}
        self._close_this_presenter_with_result(result_data, self.MANAGED_SALES_RESULT)

    def get_default_window_title(self) -> str:
        return 'Blue POS - Gestión de ventas'

    def open_filter_presenter(self):
        intent = Intent(SaleFilterPresenter)
        data = {
            SaleFilterPresenter.FILTER_BY_PRODUCT_ID_LIST_DATA: [self.__product.id],
            SaleFilterPresenter.APPLIED_FILTER: self.__applied_sale_filter
        }
        intent.set_data(data)

        intent.use_new_window(True)
        intent.use_modal(True)
        self._open_other_presenter(intent)

    def on_view_shown(self):
        self.get_view().set_product_name(self.__product.name)
        self.get_view().set_available_product_quantity(self.__product.quantity)
        self.__set_sell_button_availability_depending_on_remaining_product_quantity()
        self.get_view().disable_delete_filter_button(True)
        self.__execute_thread_to_fill_table()

    def __set_sell_button_availability_depending_on_remaining_product_quantity(self):
        if self.__product.quantity == 0:
            self.get_view().disable_sell_button(True)
        else:
            self.get_view().disable_sell_button(False)

    def __execute_thread_to_fill_table(self):
        self.thread = PresenterThreadWorker(self.__load_product_sales)
        self.thread.when_started.connect(lambda: self.get_view().show_loading_with_message('Cargando'))

        self.thread.when_finished.connect(self.__fill_table)
        self.thread.when_finished.connect(self.__set_available_gui_and_show_no_message)
        self.thread.when_finished.connect(lambda: self.get_view().hide_loading_animation())

        self.thread.start()

    def __load_product_sales(self, thread: PresenterThreadWorker):
        self.__product_sales = self.__get_sales_of_product()

    def __disable_gui_and_show_loading_sales_message(self):
        self.get_view().set_disabled_view_except_status_bar(True)
        self.get_view().set_status_bar_message('Cargando datos...')

    def __fill_table(self):
        self.get_view().clean_table()
        for a_sale in self.__product_sales:
            self.__add_sale_to_table(a_sale)

        self.get_view().sort_table_rows()
        self.get_view().resize_table_columns_to_contents()

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
        view.set_cell_in_table(row, ProductSaleManagementView.COST_COLUMN, sale.cost)
        view.set_cell_in_table(row, ProductSaleManagementView.PROFIT_COLUMN, sale.profit)
        view.set_cell_in_table(row, ProductSaleManagementView.SALE_DATE_COLUMN, sale.date)

    def __set_available_gui_and_show_no_message(self):
        self.get_view().set_disabled_view_except_status_bar(False)
        self.get_view().set_status_bar_message('')

    def undo_selected_sales(self):
        if self.get_view().ask_user_to_confirm_undo_sales():
            self.__selected_sale_id_list = self.get_view().get_selected_sale_ids()

            self.thread = PresenterThreadWorker(self.__undo_selected_sales)

            self.thread.when_started.connect(lambda: self.get_view().show_loading_with_message('Eliminando'))
            self.thread.when_finished.connect(self.get_view().delete_selected_sales_from_table)
            self.thread.when_finished.connect(self.__update_available_product_quantity_on_gui)
            self.thread.when_finished.connect(
                self.__set_sell_button_availability_depending_on_remaining_product_quantity)
            self.thread.when_finished.connect(self.get_view().resize_table_columns_to_contents)
            self.thread.when_finished.connect(self.__set_available_gui_and_show_no_message)
            self.thread.when_finished.connect(self.get_view().hide_loading_animation)
            self.thread.start()

    def __disable_gui_and_show_undoing_sales_message(self):
        self.get_view().set_disabled_view_except_status_bar(True)
        self.get_view().set_status_bar_message('Deshaciendo ventas...')

    def __update_available_product_quantity_on_gui(self):
        # Aquí no es necesario realizar ninguna substracción porque SqlAlchemy
        # se encarga de actualizar el valor de los atributos cada vez que son accedidos
        self.get_view().set_available_product_quantity(self.__product.quantity)

    def __undo_selected_sales(self, thread: PresenterThreadWorker = None):
        self.__sale_repo.delete_sales(self.__selected_sale_id_list)

    def __set_gui_available_and_show_no_message(self):
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

        if self.__applied_sale_filter is None or self.__are_sales_matching_sale_filter_values(new_sales):

            self.__disable_gui_and_show_loading_sales_message()

            for a_sale in new_sales:
                self.__add_sale_to_table(a_sale)

            self.__update_available_product_quantity_on_gui()
            self.__set_sell_button_availability_depending_on_remaining_product_quantity()
            self.__set_available_gui_and_show_no_message()
            self.get_view().resize_table_columns_to_contents()
            self.get_view().sort_table_rows()

    def __are_sales_matching_sale_filter_values(self, sales: list) -> bool:
        a_sale: Sale = sales[0]
        return (self.__applied_sale_filter is not None
                and self.__applied_sale_filter.minimum_date <= a_sale.date
                and self.__applied_sale_filter.maximum_date >= a_sale.date)

    def __update_sale_on_table(self, result_data: dict):
        selected_row = self.get_view().get_selected_row_index()
        updated_sale = result_data[EditSalePresenter.UPDATED_SALE]

        if self.__applied_sale_filter is None or self.__are_sales_matching_sale_filter_values([updated_sale]):

            self.__set_table_row_by_sale(selected_row, updated_sale)
            self.get_view().resize_table_columns_to_contents()
            self.get_view().sort_table_rows()
        elif not self.__are_sales_matching_sale_filter_values([updated_sale]):
            self.get_view().delete_selected_sales_from_table()

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
        self.thread = PresenterThreadWorker(self.__load_sale_using_filter)

        self.thread.when_started.connect(self.__disable_gui_and_show_filtering_message)

        self.thread.when_finished.connect(self.__fill_table_with_filtered_sales)
        self.thread.when_finished.connect(self.get_view().sort_table_rows)
        self.thread.when_finished.connect(self.__set_delete_filter_button_available)
        self.thread.when_finished.connect(self.get_view().resize_table_columns_to_contents)
        self.thread.when_finished.connect(
            self.__set_gui_available_and_show_filtered_sales_message)
        self.thread.start()

    def __load_sale_using_filter(self, thread: PresenterThreadWorker):
        self.__filtered_sales = self.__sale_repo.get_sales_by_filter(self.__applied_sale_filter)

    def __fill_table_with_filtered_sales(self):
        self.get_view().clean_table()
        for a_sale in self.__filtered_sales:
            self.__add_sale_to_table(a_sale)

    def __disable_gui_and_show_filtering_message(self):
        self.get_view().set_disabled_view_except_status_bar(True)
        self.get_view().set_status_bar_message('Filtrando ventas...')

    def __set_gui_available_and_show_filtered_sales_message(self):
        self.get_view().set_disabled_view_except_status_bar(False)
        self.get_view().set_filter_applied_message(True)
        self.get_view().set_status_bar_message('')

    def __set_delete_filter_button_available(self):
        self.get_view().disable_delete_filter_button(False)

    def execute_thread_to_delete_applied_filter(self):
        self.__applied_sale_filter = None
        self.thread = PresenterThreadWorker(self.__load_product_sales)

        self.thread.when_started.connect(self.__disable_gui_and_show_loading_sales_message)

        self.thread.when_finished.connect(self.__fill_table)
        self.thread.when_finished.connect(self.__set_delete_filter_button_disabled)
        self.thread.when_finished.connect(self.__show_no_filter_applied_message)
        self.thread.when_finished.connect(self.__set_gui_available_and_show_no_message)
        self.thread.start()

    def __set_delete_filter_button_disabled(self):
        self.get_view().disable_delete_filter_button(True)

    def __show_no_filter_applied_message(self):
        self.get_view().set_filter_applied_message(False)