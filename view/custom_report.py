from datetime import date

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QTableWidget, QTableWidgetItem, QToolBar, QHBoxLayout
from PyQt5.uic import loadUi

from view.util.table_columns import QIntegerTableItem
from view.util.text_tool_button import ToolButtonWithTextAndIcon
from view.util.toast import ToastView
from util.resources_path import resource_path


class CustomSaleReportView(QFrame, ToastView):

    SALE_ID_REPORT_COLUMN = 'Id. de Venta'
    PAID_REPORT_COLUMN = 'Pagado'
    PROFIT_REPORT_COLUMN = 'Ganancia'
    SALE_DATE_REPORT_COLUMN = 'Fecha'

    PRODUCT_ID_TABLE_COLUMN = 0
    PRODUCT_NAME_TABLE_COLUMN = 1

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()

    def __setup_gui(self):
        loadUi(resource_path('view/ui/custom_sale_report.ui'), self)
        self.__setup_tool_bar()
        self.__setup_date_edit()
        self.__setup_product_table()
        self.__wire_up_gui_connections()

        self.hide_state_bar()

    def __setup_tool_bar(self):
        self.set_up_tool_buttons()
        self.tool_bar = QToolBar()
        self.tool_bar_frame.setLayout(QHBoxLayout())
        self.tool_bar_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.tool_bar_frame.layout().setMenuBar(self.tool_bar)

        self.tool_bar.addWidget(self.back_button)

    def set_up_tool_buttons(self):
        self.back_button = ToolButtonWithTextAndIcon('Atrás')
        self.back_button.set_icon(QPixmap(resource_path('view/ui/images/back.png')))

    def __setup_date_edit(self):
        self.initial_date_edit.setDate(QDate.currentDate())
        self.final_date_edit.setDate(QDate.currentDate())
        self.initial_date_edit.setMaximumDate(QDate.currentDate())
        self.final_date_edit.setMaximumDate(QDate.currentDate())
        self.initial_date_edit.lineEdit().setReadOnly(True)
        self.final_date_edit.lineEdit().setReadOnly(True)
        self.final_date_edit.dateChanged.connect(
            lambda: self.initial_date_edit.setMaximumDate(self.final_date_edit.date())
        )

    def __setup_product_table(self):
        self.selected_products_table.setColumnCount(2)
        self.selected_products_table.setHorizontalHeaderLabels([
            'Id.',
            'Producto'
        ])
        self.selected_products_table.resizeColumnsToContents()
        self.selected_products_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.selected_products_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.selected_products_table.setSortingEnabled(True)

    def __wire_up_gui_connections(self):
        self.back_button.clicked.connect(self.__presenter.close_presenter)
        self.include_all_button.clicked.connect(self.__presenter.execute_thread_to_insert_all_products_on_table)
        self.edit_button.clicked.connect(self.__presenter.open_product_selection_presenter)
        self.create_report_button.clicked.connect(self.__presenter.open_custom_report_visualization_presenter)

    def get_report_name(self) -> str:
        return self.name_line_edit.text().lstrip().strip()

    def get_report_description(self) -> str:
        return self.description_plain_text_edit.document().toRawText().lstrip().rstrip()

    def get_initial_date(self) -> date:
        qdate: QDate = self.initial_date_edit.date()
        return date(day=qdate.day(),
                    month=qdate.month(),
                    year=qdate.year())

    def get_final_date(self) -> date:
        qdate: QDate = self.final_date_edit.date()
        return date(day=qdate.day(),
                    month=qdate.month(),
                    year=qdate.year())

    def get_order_by_report_column(self) -> str:
        return self.order_by_combo_box.currentText()

    def is_ascending_order(self) -> bool:
        if self.ascending_radio_button.isChecked():
            return True
        return False

    def disable_all_gui(self, disable: bool):
        self.main_content_frame.setDisabled(disable)
        self.back_button.setDisabled(disable)
        self.create_report_button.setDisabled(disable)

    def hide_state_bar(self):
        self.state_bar_label.hide()

    def show_state_bar(self):
        self.state_bar_label.show()

    def set_state_bar_message(self, text: str):
        self.state_bar_label.setText(text)

    def clean_table(self):
        while self.selected_products_table.rowCount() > 0:
            self.selected_products_table.removeRow(0)

    def add_empty_row_at_the_end_of_table(self):
        new_row_index = self.selected_products_table.rowCount()
        self.selected_products_table.insertRow(new_row_index)

    def get_last_row_index(self) -> int:
        return self.selected_products_table.rowCount() - 1

    def set_cell_in_table(self, row: int, column: int, data):

        item = QTableWidgetItem(str(data))
        if column == self.PRODUCT_ID_TABLE_COLUMN:
            item = QIntegerTableItem(str(data))

        self.selected_products_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.selected_products_table.setItem(row, column, item)

    def resize_table_columns_to_contents(self):
        self.selected_products_table.resizeColumnsToContents()


