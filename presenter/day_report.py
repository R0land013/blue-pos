from pathlib import Path
from typing import List

from easy_mvp.abstract_presenter import AbstractPresenter

from model.entity.models import Sale
from model.report.day import DaySaleReport
from model.report.generators import generate_pdf_file, generate_html_file
from model.report.statistics import ReportStatistic
from model.repository.factory import RepositoryFactory
from presenter.util.thread_worker import PresenterThreadWorker
from view.day_report import DaySaleReportView


class DaySaleReportPresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__initialize_view()
        self.__sale_repo = RepositoryFactory.get_sale_repository()
        self.__expense_repo = RepositoryFactory.get_expense_repository()
        self.__grouped_sales_repo = RepositoryFactory.get_sales_grouped_by_product_repository()
        self.__day_report:DaySaleReport = None
        self.__sales: List[Sale] = None
        self.__report_statistic: ReportStatistic = None

    def __initialize_view(self):
        view = DaySaleReportView(self)
        self._set_view(view)

    def close_presenter(self):
        self._close_this_presenter()

    def get_default_window_title(self) -> str:
        return 'Blue POS - Reporte Diario'

    def on_view_shown(self):
        self.get_view().sort_table_rows()

    def execute_thread_to_generate_report_on_gui(self):
        self.thread = PresenterThreadWorker(self.__load_all_report_data)
        self.thread.when_started.connect(self.__disable_gui_and_show_processing_message)
        self.thread.when_finished.connect(self.__fill_table)
        self.thread.when_finished.connect(self.__set_report_statistics)
        self.thread.when_finished.connect(self.__set_available_gui_and_show_no_state_bar_message)
        self.thread.start()

    def __load_all_report_data(self, thread: PresenterThreadWorker):
        self.__day_report = DaySaleReport(day_date=self.get_view().get_date(),
                                          sale_repo=self.__sale_repo,
                                          expense_repo=self.__expense_repo,
                                          grouped_sales_repo=self.__grouped_sales_repo
                                          )
        self.__sales = self.__day_report.get_sales()
        self.__expenses = self.__day_report.get_expenses()
        self.__report_statistic = self.__day_report.get_report_statistics()

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

        view.set_cell_on_table(row, DaySaleReportView.SALE_ID_COLUMN, str(sale.id))
        view.set_cell_on_table(row, DaySaleReportView.PRODUCT_NAME_COLUMN, str(sale.product.name))
        view.set_cell_on_table(row, DaySaleReportView.PRODUCT_ID_COLUMN, str(sale.product.id))
        view.set_cell_on_table(row, DaySaleReportView.SALE_PRICE_COLUMN, str(sale.price))
        view.set_cell_on_table(row, DaySaleReportView.SALE_COST_COLUMN, str(sale.cost))
        view.set_cell_on_table(row, DaySaleReportView.SALE_PROFIT_COLUMN, str(sale.profit))

    def __set_report_statistics(self):
        self.get_view().set_report_day(self.__report_statistic.initial_date())
        self.get_view().set_sale_quantity(self.__report_statistic.sale_quantity())
        self.get_view().set_paid_money(self.__report_statistic.paid_money())
        self.get_view().set_total_cost_money(self.__report_statistic.cost_money())
        self.get_view().set_profit_money(self.__report_statistic.profit_money())
        self.get_view().set_total_expense_money(self.__report_statistic.total_expenses())
        self.get_view().set_net_profit(self.__report_statistic.net_profit())

    def __set_available_gui_and_show_no_state_bar_message(self):
        self.get_view().set_disabled_view_except_status_bar(False)
        self.get_view().set_state_bar_message('')

    def ask_user_to_export_report(self):
        suggested_filename = self.__suggested_report_filename_using_date()
        self.__path, self.__file_type = self.get_view().ask_user_to_save_report_as(suggested_filename)
        self.__execute_thread_to_generate_report_file()

    def __suggested_report_filename_using_date(self) -> str:
        report_date = self.get_view().get_date()
        return 'Reporte ventas {}-{}-{}'.format(
            report_date.year,
            report_date.month,
            report_date.day
        )

    def __execute_thread_to_generate_report_file(self):
        self.thread = PresenterThreadWorker(self.__export_report_to_specified_path)
        self.thread.when_started.connect(self.__disable_gui_and_show_exporting_message)
        self.thread.when_finished.connect(self.__set_available_gui_and_show_no_state_bar_message)
        self.thread.start()

    def __export_report_to_specified_path(self, thread: PresenterThreadWorker):
        if 'pdf' in self.__file_type:
            generate_pdf_file(Path(self.__path), self.__day_report)
        elif 'html' in self.__file_type:
            generate_html_file(Path(self.__path), self.__day_report)

    def __disable_gui_and_show_exporting_message(self):
        self.get_view().set_disabled_view_except_status_bar(True)
        self.get_view().set_state_bar_message('Exportando reporte...')
