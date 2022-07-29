from easy_mvp.abstract_presenter import AbstractPresenter

from model.entity.models import Sale
from model.report.month import MonthSaleReport
from model.repository.factory import RepositoryFactory
from presenter.util.thread_worker import PresenterThreadWorker
from view.month_report import MonthSaleReportView


class MonthSaleReportPresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__initialize_view()
        self.__sale_repo = RepositoryFactory.get_sale_repository()

    def __initialize_view(self):
        self._set_view(MonthSaleReportView(self))

    def close_presenter(self):
        self._close_this_presenter()

    def execute_thread_to_generate_report_on_gui(self):
        self.thread = PresenterThreadWorker(self.__load_report_sales)
        self.thread.when_started.connect(self.__disable_gui_and_show_processing_message)
        self.thread.when_finished.connect(self.__fill_table)
        self.thread.when_finished.connect(self.__set_available_gui_and_show_no_state_bar_message)
        self.thread.start()

    def __load_report_sales(self, thread: PresenterThreadWorker):
        self.__month_report = MonthSaleReport(month_date=self.get_view().get_date(),
                                            sale_repository=self.__sale_repo)
        self.__sales = self.__month_report.get_sales()

    def __disable_gui_and_show_processing_message(self):
        self.get_view().set_disabled_view_except_status_bar(True)
        self.get_view().set_state_bar_message('Creando reporte...')

    def __fill_table(self):
        self.get_view().clean_table()
        for a_sale in self.__sales:
            self.__insert_sale_on_table(a_sale)
        self.get_view().resize_table_columns_to_contents()

    def __insert_sale_on_table(self, sale: Sale):
        view = self.get_view()
        view.add_empty_row_at_the_end_of_table()
        row = view.get_last_table_row_index()

        view.set_cell_on_table(row, MonthSaleReportView.SALE_ID_COLUMN, str(sale.id))
        view.set_cell_on_table(row, MonthSaleReportView.PRODUCT_NAME_COLUMN, str(sale.product.name))
        view.set_cell_on_table(row, MonthSaleReportView.PRODUCT_ID_COLUMN, str(sale.product.id))
        view.set_cell_on_table(row, MonthSaleReportView.SALE_PRICE_COLUMN, str(sale.price))
        view.set_cell_on_table(row, MonthSaleReportView.SALE_PROFIT_COLUMN, str(sale.profit))
        view.set_cell_on_table(row, MonthSaleReportView.SALE_DATE_COLUMN, str(sale.date))

    def __set_available_gui_and_show_no_state_bar_message(self):
        self.get_view().set_disabled_view_except_status_bar(False)
        self.get_view().set_state_bar_message('')
