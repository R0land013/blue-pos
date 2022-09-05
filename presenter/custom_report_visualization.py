from pathlib import Path
from typing import List
from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent

from model.entity.models import Expense
from model.report.custom import CustomSaleReport
from model.report.generators import generate_pdf_file, generate_html_file
from model.entity.sales_grouped_by_product import SalesGroupedByProduct
from model.report.statistics import ReportStatistic
from model.repository.factory import RepositoryFactory
from presenter.expenses_visualization import ExpensesVisualizationPresenter
from presenter.util.thread_worker import PresenterThreadWorker
from view.custom_report_visualization import CustomReportVisualizationView


class CustomReportVisualizationPresenter(AbstractPresenter):

    INITIAL_DATE_DATA = 'initial_date_data'
    FINAL_DATE_DATA = 'final_date_data'
    PRODUCT_ID_LIST_DATA = 'product_id_list_data'
    REPORT_NAME_DATA = 'report_name_data'
    REPORT_DESCRIPTION_DATA = 'report_description_data'

    def _on_initialize(self):
        self._set_view(CustomReportVisualizationView(self))
        self.__sale_repo = RepositoryFactory.get_sale_repository()
        self.__expense_repo = RepositoryFactory.get_expense_repository()
        self.__sale_group_repo = RepositoryFactory.get_sales_grouped_by_product_repository()

        self.__initial_date = self._get_intent_data()[self.INITIAL_DATE_DATA]
        self.__final_date = self._get_intent_data()[self.FINAL_DATE_DATA]
        self.__product_id_list = self._get_intent_data()[self.PRODUCT_ID_LIST_DATA]
        self.__name = self._get_intent_data()[self.REPORT_NAME_DATA]
        self.__description = self._get_intent_data()[self.REPORT_DESCRIPTION_DATA]
        self.__report: CustomSaleReport = None
        self.__sale_groups: List[SalesGroupedByProduct] = []
        self.__expenses: List[Expense] = []
        self.__report_statistic: ReportStatistic = None

    def close_presenter(self):
        self._close_this_presenter()

    def get_default_window_title(self) -> str:
        return 'Blue POS - Reporte Personalizado'

    def on_view_shown(self):
        self.__execute_thread_to_create_report_on_gui()

    def __execute_thread_to_create_report_on_gui(self):
        self.thread = PresenterThreadWorker(self.__load_all_report_data)

        self.thread.when_started.connect(self.__disable_gui_and_show_creating_report_message)

        self.thread.when_finished.connect(self.__fill_table)
        self.thread.when_finished.connect(self.__set_report_information)
        self.thread.when_finished.connect(self.__set_report_statistics)

        self.thread.when_finished.connect(lambda: self.get_view().set_state_bar_hidden(True))
        self.thread.when_finished.connect(lambda: self.get_view().disable_all_gui(False))
        self.thread.start()

    def __load_all_report_data(self, thread: PresenterThreadWorker):
        self.__report= CustomSaleReport(initial_date=self.__initial_date,
                                        final_date=self.__final_date,
                                        product_id_list=self.__product_id_list,
                                        name=self.__name,
                                        description=self.__description,
                                        sale_repository=self.__sale_repo,
                                        expense_repo=self.__expense_repo,
                                        grouped_sales_repo=self.__sale_group_repo)
        self.__sale_groups = self.__report.get_sales_grouped_by_product()
        self.__expenses = self.__report.get_expenses()
        self.__report_statistic = self.__report.get_report_statistics()

    def __disable_gui_and_show_creating_report_message(self):
        self.get_view().disable_all_gui(True)
        self.get_view().set_state_bar_message('Creando reporte...')

    def __fill_table(self):
        self.get_view().clean_table()
        for a_group_sale in self.__sale_groups:
            self.__add_sale_to_table(a_group_sale)
        self.get_view().resize_table_columns_to_contents()

    def __add_sale_to_table(self, group_sale: SalesGroupedByProduct):
        view = self.get_view()
        view.add_empty_row_at_the_end_of_table()
        row = view.get_last_table_row_index()

        view.set_cell_on_table(row, CustomReportVisualizationView.PRODUCT_ID_COLUMN, str(group_sale.product_id))
        view.set_cell_on_table(row, CustomReportVisualizationView.PRODUCT_NAME_COLUMN, str(group_sale.product_name))
        view.set_cell_on_table(row, CustomReportVisualizationView.SALE_QUANTITY_COLUMN, str(group_sale.sale_quantity))
        view.set_cell_on_table(row, CustomReportVisualizationView.ACQUIRED_MONEY_COLUMN, str(group_sale.acquired_money))
        view.set_cell_on_table(row, CustomReportVisualizationView.TOTAL_COST_COLUMN, str(group_sale.total_cost))
        view.set_cell_on_table(row, CustomReportVisualizationView.TOTAL_PROFIT_COLUMN, str(group_sale.total_profit))

    def __set_report_information(self):
        self.get_view().set_report_name(self.__name)
        self.get_view().set_report_description(self.__description)

    def __set_report_statistics(self):
        view = self.get_view()
        view.set_initial_date(self.__report_statistic.initial_date())
        view.set_final_date(self.__report_statistic.final_date())
        view.set_sale_quantity(self.__report_statistic.sale_quantity())
        view.set_paid_money(self.__report_statistic.paid_money())
        view.set_total_cost_money(self.__report_statistic.cost_money())
        view.set_profit_money(self.__report_statistic.profit_money())
        view.set_total_expense_money(self.__report_statistic.total_expenses())
        view.set_net_profit(self.__report_statistic.net_profit())

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

    def open_expenses_visualization_presenter(self):
        intent = Intent(ExpensesVisualizationPresenter)
        intent.use_new_window(True)
        intent.use_modal(True)
        intent.set_data({
            ExpensesVisualizationPresenter.INITIAL_DATE_DATA: self.__initial_date,
            ExpensesVisualizationPresenter.FINAL_DATE_DATA: self.__final_date,
            ExpensesVisualizationPresenter.TOTAL_EXPENSE_DATA: self.__report_statistic.total_expenses(),
            ExpensesVisualizationPresenter.EXPENSES_DATA: self.__expenses
        })

        self._open_other_presenter(intent)
