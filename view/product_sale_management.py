from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi


class ProductSaleManagementView(QFrame):

    SALE_ID_COLUMN = 0
    PAYMENT_COLUMN = 1
    PROFIT_COLUMN = 2
    SALE_DATE_COLUMN = 3

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.set_up_gui()

    def set_up_gui(self):
        loadUi('./view/ui/product_sale_management.ui', self)
        self.__set_table_format()
        self.__wire_up_connections()

    def __set_table_format(self):
        self.sale_table.setColumnCount(4)
        self.sale_table.setHorizontalHeaderLabels([
            'Id. Venta',
            'Pago',
            'Ganancia',
            'Fecha'
        ])
        self.sale_table.resizeColumnsToContents()
        self.sale_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.sale_table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)

    def __wire_up_connections(self):
        self.back_button.clicked.connect(self.__presenter.close_presenter)
        self.sell_button.clicked.connect(self.__presenter.open_make_sale_presenter)

    def clean_table(self):
        while self.sale_table.rowCount() > 0:
            self.sale_table.removeRow(0)

    def add_empty_row_at_the_end_of_table(self):
        new_row_index = self.sale_table.rowCount()
        self.sale_table.insertRow(new_row_index)

    def get_last_row_index(self) -> int:
        return self.sale_table.rowCount() - 1

    def set_cell_in_table(self, row: int, column: int, data):
        item = QTableWidgetItem(str(data))
        item.setData = (Qt.ItemDataRole.DisplayRole, data)
        self.sale_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.sale_table.setItem(row, column, item)

    def resize_table_columns_to_contents(self):
        self.sale_table.resizeColumnsToContents()

    def set_status_bar_message(self, message: str):
        self.state_bar_label.setText(message)

    def set_disabled_view_except_status_bar(self, disable: bool):
        self.main_content_frame.setDisabled(disable)
