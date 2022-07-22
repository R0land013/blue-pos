from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi

from view.util.table_columns import QCUPMoneyTableItem, QIntegerTableItem


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
        self.sale_table.setSortingEnabled(True)
        self.edit_sale_button.setDisabled(True)
        self.undo_sale_button.setDisabled(True)
        self.disable_delete_filter_button(True)

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
        self.undo_sale_button.clicked.connect(self.__presenter.undo_selected_sales)
        self.edit_sale_button.clicked.connect(self.__presenter.open_presenter_to_edit_sale)
        self.sale_table.itemSelectionChanged.connect(self.__disable_buttons_depending_on_table_selection)
        self.filter_button.clicked.connect(self.__presenter.open_filter_presenter)
        self.delete_filter_button.clicked.connect(self.__presenter.execute_thread_to_delete_applied_filter)

    def __disable_buttons_depending_on_table_selection(self):
        selected_sale_quantity = self.__get_selected_sale_quantity()

        if selected_sale_quantity == 1:
            self.edit_sale_button.setDisabled(False)
            self.undo_sale_button.setDisabled(False)
        elif selected_sale_quantity >= 1:
            self.edit_sale_button.setDisabled(True)
            self.undo_sale_button.setDisabled(False)
        else:
            self.edit_sale_button.setDisabled(True)
            self.undo_sale_button.setDisabled(True)

    def disable_delete_filter_button(self, set_disabled: bool):
        self.delete_filter_button.setDisabled(set_disabled)

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
        if column == self.PROFIT_COLUMN or column == self.PAYMENT_COLUMN:
            item = QCUPMoneyTableItem(str(data))
        elif column == self.SALE_ID_COLUMN:
            item = QIntegerTableItem(str(data))
        self.sale_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.sale_table.setItem(row, column, item)

    def resize_table_columns_to_contents(self):
        self.sale_table.resizeColumnsToContents()

    def set_status_bar_message(self, message: str):
        self.state_bar_label.setText(message)

    def set_disabled_view_except_status_bar(self, disable: bool):
        self.main_content_frame.setDisabled(disable)

    def set_available_product_quantity(self, quantity: int):
        self.quantity_value_label.setText(str(quantity))

    def ask_user_to_confirm_undo_sales(self) -> bool:
        message_box = self.__construct_message_box()
        pressed_button = message_box.exec()
        return pressed_button == QMessageBox.StandardButton.Ok

    def __construct_message_box(self) -> QMessageBox:
        quantity = self.__get_selected_sale_quantity()
        sale_word = self.__get_singular_or_plural_sale_word()

        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Question)
        message_box.setWindowTitle('Blue POS - Deshacer {}'.format(sale_word))
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        message_box.setText('¿Seguro que desea deshacer {} {}?'.format(quantity, sale_word))
        return message_box

    def __get_selected_sale_quantity(self) -> int:
        return len(self.sale_table.selectionModel().selectedRows(self.SALE_ID_COLUMN))

    def __get_singular_or_plural_sale_word(self):
        sale_selected_quantity = self.__get_selected_sale_quantity()
        if sale_selected_quantity == 1:
            return 'venta'
        return 'ventas'

    def get_selected_sale_ids(self) -> list:
        ids = []
        model_indexes = self.sale_table.selectionModel().selectedRows(self.SALE_ID_COLUMN)
        for a_model_index in model_indexes:
            row = a_model_index.row()
            sale_id = int(self.sale_table.item(row, self.SALE_ID_COLUMN).text())
            ids.append(sale_id)
        return ids

    def get_selected_row_index(self) -> int:
        return self.sale_table.currentRow()

    def set_filter_applied_message(self, is_filter_applied: bool):
        if is_filter_applied:
            self.filter_state_label.setText('Filtro aplicado')
        else:
            self.filter_state_label.setText('Sin Filtros')

    def disable_sell_button(self, set_disabled: bool):
        self.sell_button.setDisabled(set_disabled)

    def delete_selected_sales_from_table(self):
        model_indexes = self.sale_table.selectionModel().selectedRows(self.SALE_ID_COLUMN)
        selected_row_quantity = len(model_indexes)

        while selected_row_quantity != 0:
            a_row = model_indexes[0].row()
            self.sale_table.removeRow(a_row)

            model_indexes = self.sale_table.selectionModel().selectedRows(self.SALE_ID_COLUMN)
            selected_row_quantity = len(model_indexes)

        self.sale_table.clearSelection()
        self.__disable_buttons_depending_on_table_selection()