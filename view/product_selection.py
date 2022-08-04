from PyQt5.QtWidgets import QFrame, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi

from view.util.table_columns import QIntegerTableItem


class ProductSelectionView(QFrame):

    PRODUCT_ID_COLUMN = 0
    PRODUCT_NAME_COLUMN = 1

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/product_selection.ui', self)
        self.__setup_product_tables()
        self.send_to_selected_button.setDisabled(True)
        self.send_to_remaining_button.setDisabled(True)

        self.__wire_up_gui_connections()

    def __setup_product_tables(self):
        column_names = ['Id', 'Nombre']
        self.selected_product_table.setColumnCount(2)
        self.remaining_product_table.setColumnCount(2)
        self.selected_product_table.setHorizontalHeaderLabels(column_names)
        self.remaining_product_table.setHorizontalHeaderLabels(column_names)
        self.selected_product_table.resizeColumnsToContents()
        self.remaining_product_table.resizeColumnsToContents()
        self.selected_product_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.remaining_product_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.selected_product_table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        self.remaining_product_table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        self.selected_product_table.setSortingEnabled(True)
        self.remaining_product_table.setSortingEnabled(True)

    def __wire_up_gui_connections(self):
        self.cancel_button.clicked.connect(self.__presenter.cancel_selection_and_close_presenter)
        self.selected_product_table.itemSelectionChanged.connect(
            self.__disable_send_to_remaining_button_if_no_row_selected)
        self.remaining_product_table.itemSelectionChanged.connect(
            self.__disable_send_to_selected_button_if_no_row_selected)
        self.send_to_remaining_button.clicked.connect(
            self.__presenter.send_selected_products_to_remaining_table)
        self.send_to_selected_button.clicked.connect(
            self.__presenter.send_selected_products_to_selected_product_table
        )
        self.take_all_button.clicked.connect(self.__presenter.take_all_remaining_products)
        self.empty_button.clicked.connect(self.__presenter.empty_selected_products_table)
        self.accept_button.clicked.connect(
            self.__presenter.close_presenter_and_return_new_selected_products)

    def __disable_send_to_remaining_button_if_no_row_selected(self):
        selected_row_quantity = len(self.selected_product_table.
                                    selectionModel().selectedRows(self.PRODUCT_ID_COLUMN))
        if selected_row_quantity != 0:
            self.send_to_remaining_button.setDisabled(False)
        else:
            self.send_to_remaining_button.setDisabled(True)

    def __disable_send_to_selected_button_if_no_row_selected(self):
        selected_row_quantity = len(self.remaining_product_table.
                                    selectionModel().selectedRows(self.PRODUCT_ID_COLUMN))
        if selected_row_quantity != 0:
            self.send_to_selected_button.setDisabled(False)
        else:
            self.send_to_selected_button.setDisabled(True)

    def disable_all_gui(self, disable: bool):
        self.main_content_frame.setDisabled(disable)
        self.cancel_button.setDisabled(disable)
        self.accept_button.setDisabled(disable)

    def set_state_bar_message(self, message: str):
        self.state_bar_label.setText(message)

    def clean_selected_product_table(self):
        while self.selected_product_table.rowCount() > 0:
            self.selected_product_table.removeRow(0)

    def add_empty_row_at_the_end_of_selected_product_table(self):
        new_row_index = self.selected_product_table.rowCount()
        self.selected_product_table.insertRow(new_row_index)

    def get_last_row_index_from_selected_product_table(self) -> int:
        return self.selected_product_table.rowCount() - 1

    def set_cell_in_selected_product_table(self, row: int, column: int, data):
        item = QTableWidgetItem(str(data))
        if column == self.PRODUCT_ID_COLUMN:
            item = QIntegerTableItem(str(data))

        self.selected_product_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.selected_product_table.setItem(row, column, item)

    def resize_table_columns_to_contents_on_selected_product_table(self):
        self.selected_product_table.resizeColumnsToContents()

    def clean_remaining_product_table(self):
        while self.remaining_product_table.rowCount() > 0:
            self.remaining_product_table.removeRow(0)

    def add_empty_row_at_the_end_of_remaining_product_table(self):
        new_row_index = self.remaining_product_table.rowCount()
        self.remaining_product_table.insertRow(new_row_index)

    def get_last_row_index_from_remaining_product_table(self) -> int:
        return self.remaining_product_table.rowCount() - 1

    def set_cell_in_remaining_product_table(self, row: int, column: int, data):
        item = QTableWidgetItem(str(data))
        if column == self.PRODUCT_ID_COLUMN:
            item = QIntegerTableItem(str(data))

        self.remaining_product_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.remaining_product_table.setItem(row, column, item)

    def resize_table_columns_to_contents_on_remaining_product_table(self):
        self.remaining_product_table.resizeColumnsToContents()

    def hide_state_bar(self):
        self.state_bar_label.hide()

    def disable_take_all_button(self, disable: bool):
        self.take_all_button.setDisabled(disable)

    def disable_empty_button(self, disable: bool):
        self.empty_button.setDisabled(disable)

    def get_selected_product_ids_from_selected_product_table(self) -> list:
        ids = []
        model_indexes = self.selected_product_table.selectionModel().selectedRows(self.PRODUCT_ID_COLUMN)
        for a_model_index in model_indexes:
            row = a_model_index.row()
            product_id = int(self.selected_product_table.item(row, self.PRODUCT_ID_COLUMN).text())
            ids.append(product_id)
        return ids

    def get_selected_product_ids_from_remaining_product_table(self) -> list:
        ids = []
        model_indexes = self.remaining_product_table.selectionModel().selectedRows(self.PRODUCT_ID_COLUMN)
        for a_model_index in model_indexes:
            row = a_model_index.row()
            product_id = int(self.remaining_product_table.item(row, self.PRODUCT_ID_COLUMN).text())
            ids.append(product_id)
        return ids
