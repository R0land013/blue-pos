from datetime import date

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QTableWidget, QTableWidgetItem, QFileDialog, QToolBar, QToolButton
from PyQt5.uic import loadUi
from money import Money

from view.util.table_columns import QCUPMoneyTableItem, QIntegerTableItem
from view.util.week_selector import QWeekCalendarSelectorWidget
import os


class WeekSaleReportView(QFrame):

    PRODUCT_ID_COLUMN = 0
    PRODUCT_NAME_COLUMN = 1
    SALE_QUANTITY_COLUMN = 2
    ACQUIRED_MONEY_COLUMN = 3
    TOTAL_COST_COLUMN = 4
    TOTAL_PROFIT_COLUMN = 5

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter
        self.__sorting_column = self.TOTAL_PROFIT_COLUMN
        self.__sorting_order = Qt.AscendingOrder

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/week_sale_report.ui', self)
        self.__setup_tool_bar()
        self.__setup_week_calendar_selector()
        self.__setup_table()
        self.__wire_up_gui_connections()
        self.export_as_button.setDisabled(True)

    def __setup_tool_bar(self):
        self.set_up_tool_buttons()
        self.tool_bar = QToolBar()
        self.tool_bar_frame.setLayout(QHBoxLayout())
        self.tool_bar_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.tool_bar_frame.layout().setMenuBar(self.tool_bar)

        self.tool_bar.addWidget(self.back_button)

    def set_up_tool_buttons(self):
        self.back_button = QToolButton()
        self.back_button.setIcon(QIcon('./view/ui/images/back.png'))

    def __setup_week_calendar_selector(self):
        self.__week_calendar_selector = QWeekCalendarSelectorWidget()
        self.__week_calendar_selector.setMaximumDate(QDate.currentDate())
        self.__week_calendar_selector.setSelectedDate(QDate.currentDate())
        self.calendar_frame.setLayout(QHBoxLayout())
        self.calendar_frame.layout().addWidget(self.__week_calendar_selector)

    def __setup_table(self):
        self.sale_group_table.setColumnCount(6)
        self.sale_group_table.setHorizontalHeaderLabels([
            'Id. Producto',
            'Nombre del producto',
            'Cantidad de ventas',
            'Dinero obtenido',
            'Costo total',
            'Ganancia total',
        ])
        self.sale_group_table.resizeColumnsToContents()
        self.sale_group_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.sale_group_table.horizontalHeader().setSectionsClickable(True)

    def __wire_up_gui_connections(self):
        self.back_button.clicked.connect(self.__presenter.close_presenter)
        self.create_report_button.clicked.connect(self.__presenter.execute_thread_to_generate_report_on_gui)
        self.create_report_button.clicked.connect(lambda: self.export_as_button.setDisabled(False))
        self.create_report_button.clicked.connect(lambda: self.expenses_button.setDisabled(False))
        self.export_as_button.clicked.connect(self.__presenter.ask_user_to_export_report)
        self.sale_group_table.horizontalHeader().sectionClicked.connect(self.__change_sorting_configuration)
        self.sale_group_table.horizontalHeader().sectionClicked.connect(self.sort_table_rows)
        self.expenses_button.clicked.connect(self.__presenter.open_expenses_visualization_presenter)

    def __change_sorting_configuration(self, clicked_header_section: int):
        if clicked_header_section == self.__sorting_column:
            self.__sorting_order = (Qt.AscendingOrder if self.__sorting_order == Qt.DescendingOrder
                                    else Qt.DescendingOrder)
        else:
            self.__sorting_column = clicked_header_section
            self.__sorting_order = Qt.AscendingOrder

    def sort_table_rows(self):
        horizontal_header = self.sale_group_table.horizontalHeader()
        horizontal_header.setSortIndicator(self.__sorting_column, self.__sorting_order)
        horizontal_header.setSortIndicatorShown(True)
        self.sale_group_table.sortItems(self.__sorting_column, self.__sorting_order)

    def get_limit_dates_of_week(self) -> tuple:
        initial_qdate, final_qdate = self.__week_calendar_selector.get_selected_date_range()
        initial_py_date = date(day=initial_qdate.day(),
                               month=initial_qdate.month(),
                               year=initial_qdate.year())
        final_py_date = date(day=final_qdate.day(),
                             month=final_qdate.month(),
                             year=final_qdate.year())
        return initial_py_date, final_py_date

    def set_report_range_dates(self):
        initial_qdate, final_qdate = self.__week_calendar_selector.get_selected_date_range()
        initial_py_date = date(day=initial_qdate.day(),
                               month=initial_qdate.month(),
                               year=initial_qdate.year())
        final_py_date = date(day=final_qdate.day(),
                             month=final_qdate.month(),
                             year=final_qdate.year())
        self.__set_initial_date(initial_py_date)
        self.__set_final_date(final_py_date)

    def __set_initial_date(self, initial_date: date):
        self.initial_date_label.setText(
            '{}/{}/{}'.format(
                initial_date.day,
                initial_date.month,
                initial_date.year))

    def __set_final_date(self, final_date: date):
        self.final_date_label.setText(
            '{}/{}/{}'.format(
                final_date.day,
                final_date.month,
                final_date.year))

    def set_sale_quantity(self, quantity: int):
        self.sale_quantity_label.setText(' {}'.format(quantity))

    def set_paid_money(self, paid_money: Money):
        self.payment_money_label.setText(' {} CUP'.format(paid_money.amount))

    def set_total_cost(self, total_cost: Money):
        self.total_cost_label.setText('-{} CUP'.format(total_cost.amount))

    def set_profit_money(self, total_profit: Money):
        self.profit_money_label.setText(' {} CUP'.format(total_profit.amount))

    def set_expense_money(self, expense_money: Money):
        self.expenses_label.setText('-{} CUP'.format(expense_money.amount))

    def set_net_profit_money(self, net_profit: Money):
        if net_profit >= Money('0.00', 'CUP'):
            net_profit_text = ' {} CUP'
        else:
            net_profit_text = '{} CUP'
        self.net_profit_label.setText(net_profit_text.format(net_profit.amount))

    def set_disabled_view_except_status_bar(self, disable: bool):
        self.main_content_frame.setDisabled(disable)
        self.export_as_button.setDisabled(disable)

    def set_state_bar_message(self, message: str):
        self.state_bar_label.setText(message)

    def clean_table(self):
        while self.sale_group_table.rowCount() > 0:
            self.sale_group_table.removeRow(0)

    def add_empty_row_at_the_end_of_table(self):
        new_row_index = self.sale_group_table.rowCount()
        self.sale_group_table.insertRow(new_row_index)

    def set_cell_on_table(self, row: int, column: int, data):

        item = QTableWidgetItem(str(data))
        if column == [self.ACQUIRED_MONEY_COLUMN, self.TOTAL_COST_COLUMN, self.TOTAL_PROFIT_COLUMN]:
            item = QCUPMoneyTableItem(str(data))
        elif column == self.PRODUCT_ID_COLUMN or column == self.SALE_QUANTITY_COLUMN:
            item = QIntegerTableItem(str(data))
        self.sale_group_table.setItem(row, column, item)

    def get_last_table_row_index(self) -> int:
        return self.sale_group_table.rowCount() - 1

    def resize_table_columns_to_contents(self):
        self.sale_group_table.resizeColumnsToContents()

    def ask_user_to_save_report_as(self, suggested_file_name: str) -> tuple:
        user_home_directory = os.path.expanduser('~')
        return QFileDialog.getSaveFileName(
            parent=self.window(),
            directory=os.path.join(user_home_directory, suggested_file_name),
            caption='Exportar como',
            filter='PDF (*.pdf);;Página web (*.html *mhtml)'
        )