from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QTableWidgetItem, QTableWidget, QMessageBox, QToolBar, QHBoxLayout, QPushButton
from PyQt5.uic import loadUi
from view.util.table_columns import QCUPMoneyTableItem, QIntegerTableItem
from view.util.text_tool_button import ToolButtonWithTextAndIcon


class ProductManagementView(QFrame):

    ID_COLUMN = 0
    NAME_COLUMN = 1
    PRICE_COLUMN = 2
    COST_COLUMN = 3
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
        self.product_table.setSortingEnabled(True)
        self.edit_button.setDisabled(True)
        self.delete_button.setDisabled(True)
        self.sell_button.setDisabled(True)

    def __set_table_format(self):
        self.product_table.setColumnCount(6)
        self.product_table.setHorizontalHeaderLabels([
            'Id.',
            'Nombre',
            'Precio/u',
            'Costo/u',
            'Ganacia/u',
            'Cantidad disponible'
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
        self.tool_bar.addWidget(self.edit_button)
        self.tool_bar.addWidget(self.delete_button)

        self.tool_bar.addSeparator()
        self.tool_bar.addWidget(self.sell_button)

    def set_up_tool_buttons(self):
        self.back_button = ToolButtonWithTextAndIcon('Atrás')
        self.back_button.set_icon(QPixmap('./view/ui/images/back.png'))

        self.new_button = ToolButtonWithTextAndIcon('Añadir')
        self.new_button.set_icon(QPixmap('./view/ui/images/new.png'))

        self.edit_button = ToolButtonWithTextAndIcon('Editar')
        self.edit_button.set_icon(QPixmap('./view/ui/images/edit.png'))

        self.delete_button = ToolButtonWithTextAndIcon('Eliminar')
        self.delete_button.set_icon(QPixmap('./view/ui/images/delete.png'))

        self.sell_button = ToolButtonWithTextAndIcon('Ventas')
        self.sell_button.set_icon(QPixmap('./view/ui/images/sale.png'))

    def __wire_up_gui_connections(self):
        self.back_button.clicked.connect(self.__presenter.return_to_main)
        self.new_button.clicked.connect(self.__presenter.open_presenter_to_create_new_product)
        self.edit_button.clicked.connect(self.__presenter.open_presenter_to_edit_product)
        self.delete_button.clicked.connect(self.__presenter.delete_selected_product)
        self.sell_button.clicked.connect(self.__presenter.open_product_sale_management_presenter)
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
        if column == self.PROFIT_COLUMN or column == self.PRICE_COLUMN:
            item = QCUPMoneyTableItem(str(data))
        elif column == self.QUANTITY_COLUMN or column == self.ID_COLUMN:
            item = QIntegerTableItem(str(data))

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
        detail_message = '¿Seguro que desea borrar {} {}?\nSe eliminarán todas sus ventas asociadas.'\
            .format(product_quantity, product_text)

        message_box = QMessageBox(self.window())
        message_box.setIcon(QMessageBox.Question)
        message_box.setText(detail_message)
        message_box.setWindowTitle('Eliminar productos')

        delete_button = QPushButton('Eliminar')
        delete_button.setObjectName('dialog_delete_button')
        delete_button.setCursor(Qt.PointingHandCursor)
        message_box.addButton(delete_button, QMessageBox.AcceptRole)

        cancel_button = QPushButton('Cancelar')
        cancel_button.setCursor(Qt.PointingHandCursor)
        message_box.addButton(cancel_button, QMessageBox.NoRole)

        message_box.exec()
        if message_box.clickedButton() == delete_button:
            return True
        return False
