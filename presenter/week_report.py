from pathlib import Path
from typing import List

from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent

from model.entity.models import Expense
from model.report.generators import generate_pdf_file, generate_html_file
from model.entity.sales_grouped_by_product import SalesGroupedByProduct
from model.report.statistics import ReportStatistic
from model.report.week import WeekSaleReport
from model.repository.factory import RepositoryFactory
from presenter.expenses_visualization import ExpensesVisualizationPresenter
from presenter.util.thread_worker import PresenterThreadWorker
from view.week_report import WeekSaleReportView
from model.report.generators import DirectoryPermissionError


class WeekSaleReportPresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__sale_repo = RepositoryFactory.get_sale_repository()
        self.__sale_group_repo = RepositoryFactory.get_sales_grouped_by_product_repository()
        self.__expense_repo = RepositoryFactory.get_expense_repository()
        self.__report_statistic: ReportStatistic = None
        self.__sales_grouped_by_product_list: List[SalesGroupedByProduct] = None
        self.__expenses: List[Expense] = None
        self._set_view(WeekSaleReportView(self))

    def close_presenter(self):
        self._close_this_presenter()

    def get_default_window_title(self) -> str:
        return 'Blue POS - Reporte Semanal'

    def execute_thread_to_generate_report_on_gui(self):
        self.thread = PresenterThreadWorker(self.__load_all_report_data)
        self.thread.when_started.connect(self.__disable_gui_and_show_processing_message)
        self.thread.when_finished.connect(self.__fill_table)
        self.thread.when_finished.connect(self.get_view().sort_table_rows)
        self.thread.when_finished.connect(self.__set_report_statistics)
        self.thread.when_finished.connect(self.__set_available_gui_and_show_no_state_bar_message)
        self.thread.start()

    def __load_all_report_data(self, thread: PresenterThreadWorker):
        """
        Crea el reporte, carga las ventas agrupadas por producto, crea las estadísticas
        del reporte y carga la lista de gastos.
        """
        initial_date, final_date = self.get_view().get_limit_dates_of_week()
        self.__week_report = WeekSaleReport(week_day=initial_date, sale_repository=self.__sale_repo,
                                            grouped_sales_repo=self.__sale_group_repo,
                                            expense_repo=self.__expense_repo)
        self.__sales_grouped_by_product_list = self.__week_report.get_sales_grouped_by_product()
        self.__report_statistic = self.__week_report.get_report_statistics()
        self.__expenses = self.__week_report.get_expenses()

    def __disable_gui_and_show_processing_message(self):
        self.get_view().set_disabled_view_except_status_bar(True)
        self.get_view().set_state_bar_message('Creando reporte...')

    def __fill_table(self):
        self.get_view().clean_table()
        for a_sale_group in self.__sales_grouped_by_product_list:
            self.__insert_sale_on_table(a_sale_group)
        self.get_view().resize_table_columns_to_contents()

    def __insert_sale_on_table(self, sale_group: SalesGroupedByProduct):
        view = self.get_view()
        view.add_empty_row_at_the_end_of_table()
        row = view.get_last_table_row_index()

        view.set_cell_on_table(row, WeekSaleReportView.PRODUCT_ID_COLUMN, str(sale_group.product_id))
        view.set_cell_on_table(row, WeekSaleReportView.PRODUCT_NAME_COLUMN, str(sale_group.product_name))
        view.set_cell_on_table(row, WeekSaleReportView.SALE_QUANTITY_COLUMN, str(sale_group.sale_quantity))
        view.set_cell_on_table(row, WeekSaleReportView.ACQUIRED_MONEY_COLUMN, str(sale_group.acquired_money))
        view.set_cell_on_table(row, WeekSaleReportView.TOTAL_COST_COLUMN, str(sale_group.total_cost))
        view.set_cell_on_table(row, WeekSaleReportView.TOTAL_PROFIT_COLUMN, str(sale_group.total_profit))

    def __set_report_statistics(self):
        self.get_view().set_report_range_dates()

        self.get_view().set_sale_quantity(self.__report_statistic.sale_quantity())
        self.get_view().set_paid_money(self.__report_statistic.paid_money())
        self.get_view().set_total_cost(self.__report_statistic.cost_money())
        self.get_view().set_profit_money(self.__report_statistic.profit_money())

        self.get_view().set_expense_money(self.__report_statistic.total_expenses())
        self.get_view().set_net_profit_money(self.__report_statistic.net_profit())

    def __set_available_gui_and_show_no_state_bar_message(self):
        self.get_view().set_disabled_view_except_status_bar(False)
        self.get_view().set_state_bar_message('')

    def ask_user_to_export_report(self):
        suggested_filename = self.__suggested_report_filename_using_date()
        self.__path, self.__file_type = self.get_view().ask_user_to_save_report_as(suggested_filename)
        self.__execute_thread_to_generate_report_file()

    def __suggested_report_filename_using_date(self) -> str:
        initial_date, final_date = self.get_view().get_limit_dates_of_week()
        return 'Reporte ventas semana {}-{}-{}'.format(
            initial_date.year,
            initial_date.month,
            initial_date.day
        )

    def __execute_thread_to_generate_report_file(self):
        self.thread = PresenterThreadWorker(self.__export_report_to_specified_path)
        self.thread.when_started.connect(self.__disable_gui_and_show_exporting_message)
        self.thread.when_finished.connect(self.__set_available_gui_and_show_no_state_bar_message)
        self.thread.error_found.connect(self.__handle_export_report_errors)
        self.thread.start()

    def __export_report_to_specified_path(self, thread: PresenterThreadWorker):
        try:
            if 'pdf' in self.__file_type:
                generate_pdf_file(Path(self.__path), self.__week_report)
            elif 'html' in self.__file_type:
                generate_html_file(Path(self.__path), self.__week_report)
        
        except DirectoryPermissionError as error:
            thread.error_found.emit(error)

    def __disable_gui_and_show_exporting_message(self):
        self.get_view().set_disabled_view_except_status_bar(True)
        self.get_view().set_state_bar_message('Exportando reporte...')

    def __handle_export_report_errors(self, error):
        if isinstance(error, DirectoryPermissionError):
            self.get_view().show_error_message('No se puede exportar el reporte hacia la carpeta seleccionada.')

    def open_expenses_visualization_presenter(self):
        intent = Intent(ExpensesVisualizationPresenter)
        intent.use_new_window(True)
        intent.use_modal(True)

        initial_date, final_date = self.get_view().get_limit_dates_of_week()
        intent.set_data({
            ExpensesVisualizationPresenter.INITIAL_DATE_DATA: initial_date,
            ExpensesVisualizationPresenter.FINAL_DATE_DATA: final_date,
            ExpensesVisualizationPresenter.TOTAL_EXPENSE_DATA: self.__report_statistic.total_expenses(),
            ExpensesVisualizationPresenter.EXPENSES_DATA: self.__expenses
        })

        self._open_other_presenter(intent)