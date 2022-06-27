from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QTableWidgetItem, QTableWidget, QMessageBox, QToolBar, QToolButton, QHBoxLayout
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
        self.__set_up_tool_bar()
        self.__wire_up_gui_connections()
        self.edit_button.setDisabled(True)
        self.delete_button.setDisabled(True)

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
        self.product_table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)

    def __set_up_tool_bar(self):
        self.set_up_tool_buttons()
        self.tool_bar = QToolBar()
        self.tool_bar_frame.setLayout(QHBoxLayout())
        self.tool_bar_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.tool_bar_frame.layout().setMenuBar(self.tool_bar)

        self.tool_bar.addWidget(self.back_button)
        self.tool_bar.addSeparator()
        self.tool_bar.addWidget(self.new_button)
        self.tool_bar.addSeparator()
        self.tool_bar.addWidget(self.edit_button)
        self.tool_bar.addSeparator()
        self.tool_bar.addWidget(self.delete_button)
        self.tool_bar.addSeparator()
        self.tool_bar.addWidget(self.sell_button)

    def set_up_tool_buttons(self):
        self.back_button = QToolButton()
        self.back_button.setIcon(QIcon('./view/ui/images/back.png'))
        self.new_button = QToolButton()
        self.new_button.setIcon(QIcon('./view/ui/images/new.png'))
        self.edit_button = QToolButton()
        self.edit_button.setIcon(QIcon('./view/ui/images/edit.png'))
        self.delete_button = QToolButton()
        self.delete_button.setIcon(QIcon('./view/ui/images/delete.png'))
        self.sell_button = QToolButton()
        self.sell_button.setIcon(QIcon('./view/ui/images/sale.png'))

    def __wire_up_gui_connections(self):
        self.back_button.clicked.connect(self.__presenter.return_to_main)
        self.new_button.clicked.connect(self.__presenter.open_presenter_to_create_new_product)
        self.edit_button.clicked.connect(self.__presenter.open_presenter_to_edit_product)
        self.delete_button.clicked.connect(self.__presenter.delete_selected_product)
        self.product_table.itemSelectionChanged.connect(self.__disable_edit_and_delete_buttons_if_no_row_selected)
        self.product_table.itemDoubleClicked.connect(self.__presenter.open_presenter_to_edit_product)

    def __disable_edit_and_delete_buttons_if_no_row_selected(self):
        selected_row_quantity = len(self.product_table.selectionModel().selectedRows(self.ID_COLUMN))

        if selected_row_quantity == 1:
            self.edit_button.setDisabled(False)
            self.delete_button.setDisabled(False)
            self.sell_button.setDisabled(False)
        elif selected_row_quantity >= 1:
            self.edit_button.setDisabled(True)
            self.delete_button.setDisabled(False)
            self.sell_button.setDisabled(True)
        else:
            self.edit_button.setDisabled(True)
            self.delete_button.setDisabled(True)
            self.sell_button.setDisabled(True)

    def set_cell_in_table(self, row: int, column: int, data):
        item = QTableWidgetItem(str(data))
        item.setData = (Qt.ItemDataRole.DisplayRole, data)
        self.product_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
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

    def get_all_selected_product_ids(self) -> list:
        ids = []
        model_indexes = self.product_table.selectionModel().selectedRows(self.ID_COLUMN)
        for a_model_index in model_indexes:
            row = a_model_index.row()
            product_id = int(self.product_table.item(row, self.ID_COLUMN).text())
            ids.append(product_id)
        return ids

    def set_disabled_view_except_status_bar(self, disable: bool):
        self.main_content_frame.setDisabled(disable)

    def set_state_bar_message(self, message: str):
        self.state_bar_label.setText(message)

    def delete_selected_products_from_table(self):
        model_indexes = self.product_table.selectionModel().selectedRows(self.ID_COLUMN)
        selected_row_quantity = len(model_indexes)

        while selected_row_quantity != 0:
            a_row = model_indexes[0].row()
            self.product_table.removeRow(a_row)

            model_indexes = self.product_table.selectionModel().selectedRows(self.ID_COLUMN)
            selected_row_quantity = len(model_indexes)

        self.product_table.clearSelection()
        self.__disable_edit_and_delete_buttons_if_no_row_selected()

    def get_last_row_index(self) -> int:
        return self.product_table.rowCount() - 1

    def get_selected_row_index(self) -> int:
        return self.product_table.currentRow()

    def ask_user_to_confirm_product_deletion(self) -> bool:
        product_quantity = len(self.product_table.selectionModel().selectedRows(self.ID_COLUMN))
        product_text = 'producto'
        if product_quantity > 1:
            product_text = 'productos'
        detail_message = '¿Seguro que desea borrar {} {}?'.format(product_quantity, product_text)
        pressed_button = QMessageBox.question(self.window(),
                                              'Blue POS - Eliminar productos',
                                              detail_message,
                                              QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        if pressed_button == QMessageBox.StandardButton.Ok:
            return True
        return False
