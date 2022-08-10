from datetime import date
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QTableWidget, QTableWidgetItem, QFileDialog, QToolBar, QHBoxLayout, QToolButton
from PyQt5.uic import loadUi
from view.util.table_columns import QCUPMoneyTableItem, QIntegerTableItem
import os


class MonthSaleReportView(QFrame):

    SALE_ID_COLUMN = 0
    PRODUCT_NAME_COLUMN = 1
    PRODUCT_ID_COLUMN = 2
    SALE_PRICE_COLUMN = 3
    SALE_PROFIT_COLUMN = 4
    SALE_DATE_COLUMN = 5

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter
        self.__sorting_column = self.SALE_DATE_COLUMN
        self.__sorting_order = Qt.DescendingOrder

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/month_sale_report.ui', self)
        self.__setup_tool_bar()
        self.__wire_up_gui_connections()
        self.__setup_date_edit()
        self.__setup_table()
        self.__disable_export_as_button()

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

    def __setup_table(self):
        self.sale_report_table.setColumnCount(6)
        self.sale_report_table.setHorizontalHeaderLabels([
            'Id. Venta',
            'Producto',
            'Id. Producto',
            'Pagado',
            'Ganancia',
            'Fecha'
        ])
        self.sale_report_table.resizeColumnsToContents()
        self.sale_report_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.sale_report_table.horizontalHeader().setSectionsClickable(True)

    def __setup_date_edit(self):
        self.month_date_edit.setDate(QDate.currentDate())
        self.month_date_edit.setMaximumDate(QDate.currentDate())

    def __wire_up_gui_connections(self):
        self.back_button.clicked.connect(self.__presenter.close_presenter)
        self.create_report_button.clicked.connect(self.__presenter.execute_thread_to_generate_report_on_gui)
        self.create_report_button.clicked.connect(self.__set_available_export_as_button)
        self.export_as_button.clicked.connect(self.__presenter.ask_user_to_export_report)
        self.month_date_edit.dateChanged.connect(self.__disable_export_as_button)
        self.sale_report_table.horizontalHeader().sectionClicked.connect(self.__change_sorting_configuration)
        self.sale_report_table.horizontalHeader().sectionClicked.connect(self.sort_table_rows)

    def __set_available_export_as_button(self):
        self.export_as_button.setDisabled(False)

    def __change_sorting_configuration(self, clicked_header_section: int):
        if clicked_header_section == self.__sorting_column:
            self.__sorting_order = (Qt.AscendingOrder if self.__sorting_order == Qt.DescendingOrder
                                    else Qt.DescendingOrder)
        else:
            self.__sorting_column = clicked_header_section
            self.__sorting_order = Qt.AscendingOrder

    def sort_table_rows(self):
        horizontal_header = self.sale_report_table.horizontalHeader()
        horizontal_header.setSortIndicator(self.__sorting_column, self.__sorting_order)
        horizontal_header.setSortIndicatorShown(True)
        self.sale_report_table.sortItems(self.__sorting_column, self.__sorting_order)

    def __disable_export_as_button(self):
        self.export_as_button.setDisabled(True)

    def get_date(self):
        q_date = self.month_date_edit.date()
        return date(day=q_date.day(),
                    month=q_date.month(),
                    year=q_date.year())

    def set_sale_quantity(self, quantity: int):
        self.sale_quantity_label.setText(str(quantity))

    def set_paid_money(self, paid: str):
        self.payment_money_label.setText(paid)

    def set_profit_money(self, profit: str):
        self.profit_money_label.setText(profit)

    def set_disabled_view_except_status_bar(self, disable: bool):
        self.main_content_frame.setDisabled(disable)
        self.export_as_button.setDisabled(disable)

    def set_state_bar_message(self, message: str):
        self.state_bar_label.setText(message)

    def clean_table(self):
        while self.sale_report_table.rowCount() > 0:
            self.sale_report_table.removeRow(0)

    def add_empty_row_at_the_end_of_table(self):
        new_row_index = self.sale_report_table.rowCount()
        self.sale_report_table.insertRow(new_row_index)

    def set_cell_on_table(self, row: int, column: int, data):

        item = QTableWidgetItem(str(data))
        if column == self.SALE_PRICE_COLUMN or column == self.SALE_PROFIT_COLUMN:
            item = QCUPMoneyTableItem(str(data))
        elif column == self.SALE_ID_COLUMN or column == self.PRODUCT_ID_COLUMN:
            item = QIntegerTableItem(str(data))
        self.sale_report_table.setItem(row, column, item)

    def get_last_table_row_index(self) -> int:
        return self.sale_report_table.rowCount() - 1

    def resize_table_columns_to_contents(self):
        self.sale_report_table.resizeColumnsToContents()

    def ask_user_to_save_report_as(self, suggested_file_name: str) -> tuple:
        user_home_directory = os.path.expanduser('~')
        return QFileDialog.getSaveFileName(
            parent=self.window(),
            directory=os.path.join(user_home_directory, suggested_file_name),
            caption='Exportar como',
            filter='PDF (*.pdf);;Página web (*.html *mhtml)'
        )
