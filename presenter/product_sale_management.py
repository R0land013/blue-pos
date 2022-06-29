from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent

from model.entity.models import Sale
from model.repository.factory import RepositoryFactory
from model.repository.sale import SaleFilter
from presenter.edit_sale import EditSalePresenter
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

    def close_presenter(self):
        self._close_this_presenter()

    def on_view_shown(self):
        self.get_view().set_available_product_quantity(self.__product.quantity)
        self.__execute_thread_to_fill_table()

    def __execute_thread_to_fill_table(self):
        self.thread = PresenterThreadWorker(self.fill_table)
        self.thread.start()

    def fill_table(self, thread: PresenterThreadWorker = None):
        self.get_view().set_disabled_view_except_status_bar(True)
        self.get_view().set_status_bar_message('Cargando datos...')
        self.get_view().clean_table()

        product_sales = self.__get_sales_of_product()
        for a_sale in product_sales:
            self.__add_sale_to_table(a_sale)

        self.get_view().resize_table_columns_to_contents()
        self.get_view().set_disabled_view_except_status_bar(False)
        self.get_view().set_status_bar_message('Datos cargados')

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

    def undo_selected_sales(self):
        if self.get_view().ask_user_to_confirm_undo_sales():
            self.thread = PresenterThreadWorker(self.__undo_selected_sales)
            self.thread.when_finished.connect(self.fill_table)
            self.thread.start()

    def __update_available_product_quantity_on_gui(self):
        # Aquí no es necesario realizar ninguna substracción porque SqlAlchemy
        # se encarga de actualizar el valor de los atributos cada vez que son accedidos
        self.get_view().set_available_product_quantity(self.__product.quantity)

    def __undo_selected_sales(self, thread: PresenterThreadWorker = None):
        self.get_view().set_disabled_view_except_status_bar(True)
        self.get_view().set_status_bar_message('Procesando...')

        mock_sales = self.__construct_mock_sales_to_execute_deletion()
        for a_mock_sale in mock_sales:
            self.__sale_repo.delete_sale(a_mock_sale)

        self.__update_available_product_quantity_on_gui()
        self.get_view().set_disabled_view_except_status_bar(False)

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
            self.__update_gui_on_new_sales_inserted()

    def __update_gui_on_new_sales_inserted(self):
        self.__execute_thread_to_fill_table()
        self.__update_available_product_quantity_on_gui()

    def open_presenter_to_edit_sale(self):
        data = {EditSalePresenter.SALE: self.__get_selected_sale()}
        intent = Intent(EditSalePresenter)
        intent.set_data(data)
        self._open_other_presenter(intent)

    def __get_selected_sale(self) -> Sale:
        sale_id = self.get_view().get_selected_sale_ids()[0]
        filter_by_id = SaleFilter()
        filter_by_id.sale_id_list = [sale_id]
        return self.__sale_repo.get_sales_by_filter(filter_by_id)[0]
