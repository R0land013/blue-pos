from pathlib import Path

from easy_mvp.abstract_presenter import AbstractPresenter

from model.entity.models import Sale
from model.report.custom import CustomSaleReport
from model.report.generators import generate_pdf_file, generate_html_file
from model.repository.factory import RepositoryFactory
from model.repository.sale import SaleFilter
from presenter.util.thread_worker import PresenterThreadWorker
from view.custom_report_visualization import CustomReportVisualizationView


class CustomReportVisualizationPresenter(AbstractPresenter):

    CUSTOM_FILTER_DATA = 'custom_filter'
    REPORT_NAME_DATA = 'report_name_data'
    REPORT_DESCRIPTION_DATA = 'report_description_data'

    def _on_initialize(self):
        self._set_view(CustomReportVisualizationView(self))
        self.__sale_repo = RepositoryFactory.get_sale_repository()
        self.__filter: SaleFilter = self._get_intent_data()[self.CUSTOM_FILTER_DATA]
        self.__name = self._get_intent_data()[self.REPORT_NAME_DATA]
        self.__description = self._get_intent_data()[self.REPORT_DESCRIPTION_DATA]
        self.__sales: list = []

    def close_presenter(self):
        self._close_this_presenter()

    def on_view_shown(self):
        self.__execute_thread_to_create_report_on_gui()

    def __execute_thread_to_create_report_on_gui(self):
        self.thread = PresenterThreadWorker(self.__load_sales_using_filter)

        self.thread.when_started.connect(self.__disable_gui_and_show_creating_report_message)

        self.thread.when_finished.connect(self.__fill_table)
        self.thread.when_finished.connect(self.__set_report_information)
        self.thread.when_finished.connect(self.__set_report_statistics)
        self.thread.when_finished.connect(lambda: self.get_view().set_state_bar_hidden(True))
        self.thread.when_finished.connect(lambda: self.get_view().disable_all_gui(False))
        self.thread.start()

    def __load_sales_using_filter(self, thread: PresenterThreadWorker):
        self.__custom_report = CustomSaleReport(self.__filter, self.__sale_repo,
                                                self.__name, self.__description)
        self.__sales = self.__custom_report.get_sales()

    def __disable_gui_and_show_creating_report_message(self):
        self.get_view().disable_all_gui(True)
        self.get_view().set_state_bar_message('Creando reporte...')

    def __fill_table(self):
        self.get_view().clean_table()
        for a_sale in self.__sales:
            self.__add_sale_to_table(a_sale)
        self.get_view().resize_table_columns_to_contents()

    def __add_sale_to_table(self, sale: Sale):
        view = self.get_view()
        view.add_empty_row_at_the_end_of_table()
        row = view.get_last_table_row_index()

        view.set_cell_on_table(row, CustomReportVisualizationView.SALE_ID_COLUMN, str(sale.id))
        view.set_cell_on_table(row, CustomReportVisualizationView.PRODUCT_NAME_COLUMN, str(sale.product.name))
        view.set_cell_on_table(row, CustomReportVisualizationView.PRODUCT_ID_COLUMN, str(sale.product.id))
        view.set_cell_on_table(row, CustomReportVisualizationView.SALE_PRICE_COLUMN, str(sale.price))
        view.set_cell_on_table(row, CustomReportVisualizationView.SALE_PROFIT_COLUMN, str(sale.profit))
        view.set_cell_on_table(row, CustomReportVisualizationView.SALE_DATE_COLUMN, str(sale.date))

    def __set_report_information(self):
        self.get_view().set_report_name(self.__name)
        self.get_view().set_report_description(self.__description)

    def __set_report_statistics(self):
        report_statistics = self.__custom_report.get_report_statistics()
        view = self.get_view()
        view.set_initial_date(report_statistics.initial_date())
        view.set_final_date(report_statistics.final_date())
        view.set_sale_quantity(report_statistics.sale_quantity())
        view.set_paid_money(str(report_statistics.paid_money()))
        view.set_profit_money(str(report_statistics.profit_money()))

    def ask_user_to_export_report(self):
        suggested_filename = self.__suggested_report_filename_using_date()
        self.__path, self.__file_type = self.get_view().ask_user_to_save_report_as(suggested_filename)
        self.__execute_thread_to_generate_report_file()

    def __suggested_report_filename_using_date(self) -> str:
        initial_date = self.__custom_report.get_report_statistics().initial_date()
        final_date = self.__custom_report.get_report_statistics().final_date()
        if self.__name == '':
            return 'Reporte ventas {}-{}-{}  {}-{}-{}'.format(
                initial_date.year,
                initial_date.month,
                initial_date.day,
                final_date.year,
                final_date.month,
                final_date.day,
            )
        else:
            return 'Reporte {}'.format(self.__name)

    def __execute_thread_to_generate_report_file(self):
        self.thread = PresenterThreadWorker(self.__export_report_to_specified_path)
        self.thread.when_started.connect(self.__disable_gui_and_show_exporting_message)
        self.thread.when_finished.connect(lambda: self.get_view().set_state_bar_hidden(True))
        self.thread.when_finished.connect(lambda: self.get_view().disable_all_gui(False))
        self.thread.start()

    def __export_report_to_specified_path(self, thread: PresenterThreadWorker):
        if 'pdf' in self.__file_type:
            generate_pdf_file(Path(self.__path), self.__custom_report)
        elif 'html' in self.__file_type:
            generate_html_file(Path(self.__path), self.__custom_report)

    def __disable_gui_and_show_exporting_message(self):
        self.get_view().disable_all_gui(True)
        self.get_view().set_state_bar_hidden(False)
        self.get_view().set_state_bar_message('Exportando reporte...')
