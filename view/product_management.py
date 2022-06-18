from PyQt5.QtWidgets import QFrame, QTableWidgetItem, QTableWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt


class ProductManagementView(QFrame):

    ID_COLUMN = 0
    NAME_COLUMN = 1
    DESCRIPTION_COLUMN = 2
    PRICE_COLUMN = 3
    PROFIT_COLUMN = 4
    QUANTITY_COLUMN = 5

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        loadUi('./view/ui/product_management.ui', self)
        self.__prepare_gui()

    def __prepare_gui(self):
        self.__set_table_format()
        self.__wire_up_gui_connections()
        self.edit_button.setDisabled(True)

    def __set_table_format(self):
        self.product_table.setColumnCount(6)
        self.product_table.setHorizontalHeaderLabels([
            'Id.',
            'Nombre',
            'Descripción',
            'Precio/u',
            'Ganacia/u',
            'Cantidad'
        ])
        self.product_table.resizeColumnsToContents()
        self.product_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.product_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

    def __wire_up_gui_connections(self):
        self.back_button.clicked.connect(self.__presenter.return_to_main)
        self.new_button.clicked.connect(self.__presenter.open_presenter_to_create_new_product)
        self.edit_button.clicked.connect(self.__presenter.open_presenter_to_edit_product)
        self.product_table.itemSelectionChanged.connect(self.__disable_edit_button_if_no_row_selected)

    def __disable_edit_button_if_no_row_selected(self):
        if not self.product_table.selectionModel().hasSelection():
            self.edit_button.setDisabled(True)
        else:
            self.edit_button.setDisabled(False)

    def set_cell_in_table(self, row: int, column: int, data):
        item = QTableWidgetItem(str(data))
        item.setData = (Qt.ItemDataRole.DisplayRole, data)
        self.product_table.setItem(row, column, item)

    def add_empty_row_at_the_end_of_table(self):
        new_row_index = self.product_table.rowCount()
        self.product_table.insertRow(new_row_index)

    def resize_table_columns_to_contents(self):
        self.product_table.resizeColumnsToContents()

    def clean_table(self):
        while self.product_table.rowCount() > 0:
            self.product_table.removeRow(0)

    def get_selected_product_id(self) -> int:
        row = self.product_table.currentRow()
        if row == -1:
            return -1

        product_id = int(self.product_table.item(row, self.ID_COLUMN).text())
        return product_id
