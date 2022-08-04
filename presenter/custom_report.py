from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent

from model.entity.models import Product
from model.repository.factory import RepositoryFactory
from model.repository.sale import SaleFilter
from presenter.product_selection import ProductSelectionPresenter
from presenter.util.thread_worker import PresenterThreadWorker
from view.custom_report import CustomSaleReportView


class CustomSaleReportPresenter(AbstractPresenter):

    def _on_initialize(self):
        self._set_view(CustomSaleReportView(self))
        self.__product_repo = RepositoryFactory.get_product_repository()
        self.__selected_products = []

    def close_presenter(self):
        self._close_this_presenter()

    def open_custom_report_visualizer_presenter(self):
        sale_filter = self.__create_sale_filter()
        print("""
        name: '{}',
        description: '{}',
        minimum_date: {},
        maximum_date: {},
        product_id_list: {},
        sorted_by: {},
        ascending_order: {}
        """.format(
            self.get_view().get_report_name(),
            self.get_view().get_report_description(),
            sale_filter.minimum_date,
            sale_filter.maximum_date,
            sale_filter.product_id_list,
            sale_filter.sorted_by,
            sale_filter.ascending_order
        ))

    def __create_sale_filter(self) -> SaleFilter:
        sale_filter = SaleFilter()
        sale_filter.minimum_date = self.get_view().get_initial_date()
        sale_filter.maximum_date = self.get_view().get_final_date()
        sale_filter.sorted_by = self.__get_column_to_order_sale_report()
        sale_filter.ascending_order = self.get_view().is_ascending_order()
        sale_filter.product_id_list = list(map(lambda x: x.id, self.__selected_products))
        return sale_filter

    def __get_column_to_order_sale_report(self):
        column = self.get_view().get_order_by_report_column()
        if column == CustomSaleReportView.SALE_ID_REPORT_COLUMN:
            return SaleFilter.ID
        elif column == CustomSaleReportView.PAID_REPORT_COLUMN:
            return SaleFilter.PRICE
        elif column == CustomSaleReportView.PROFIT_REPORT_COLUMN:
            return SaleFilter.PROFIT
        return SaleFilter.SALE_DATE

    def execute_thread_to_insert_all_products_on_table(self):
        self.thread = PresenterThreadWorker(self.__load_all_products)
        self.thread.when_started.connect(self.__disable_gui_and_show_loading_products_message)
        self.thread.when_finished.connect(self.__fill_product_table)
        self.thread.when_finished.connect(self.__set_all_gui_available_and_hide_state_bar)
        self.thread.start()

    def __load_all_products(self, thread: PresenterThreadWorker):
        self.__selected_products = self.__product_repo.get_all_products()

    def __disable_gui_and_show_loading_products_message(self):
        self.get_view().disable_all_gui(True)
        self.get_view().show_state_bar()
        self.get_view().set_state_bar_message('Cargando productos...')

    def __fill_product_table(self):
        self.get_view().clean_table()
        for a_product in self.__selected_products:
            self.__add_product_to_table(a_product)
        self.get_view().resize_table_columns_to_contents()

    def __add_product_to_table(self, a_product: Product):
        view = self.get_view()
        view.add_empty_row_at_the_end_of_table()
        row = view.get_last_row_index()

        view.set_cell_in_table(row, CustomSaleReportView.PRODUCT_ID_TABLE_COLUMN, a_product.id)
        view.set_cell_in_table(row, CustomSaleReportView.PRODUCT_NAME_TABLE_COLUMN, a_product.name)

    def __set_all_gui_available_and_hide_state_bar(self):
        self.get_view().disable_all_gui(False)
        self.get_view().hide_state_bar()

    def open_product_selection_presenter(self):
        intent = Intent(ProductSelectionPresenter)
        intent.use_new_window(True)
        intent.use_modal(True)
        intent.set_data({ProductSelectionPresenter.SELECTED_PRODUCTS_DATA: self.__selected_products})
        self._open_other_presenter(intent)

    def on_view_discovered_with_result(self, action: str, result_data: dict, result: str):
        if result == ProductSelectionPresenter.NEW_SELECTED_PRODUCTS_RESULT:
            self.__selected_products = result_data[ProductSelectionPresenter.NEW_SELECTED_PRODUCTS_DATA]
            self.__fill_product_table()
