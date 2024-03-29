from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QTableWidget, QTableWidgetItem, QMessageBox, QToolBar, QHBoxLayout, \
    QPushButton
from PyQt5.uic import loadUi
from view.util.table_columns import QCUPMoneyTableItem, QIntegerTableItem
from view.util.text_tool_button import ToolButtonWithTextAndIcon
from view.util.toast import ToastView
from util.resources_path import resource_path


class ProductSaleManagementView(QFrame, ToastView):

    SALE_ID_COLUMN = 0
    PAYMENT_COLUMN = 1
    COST_COLUMN = 2
    PROFIT_COLUMN = 3
    SALE_DATE_COLUMN = 4

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter
        self.__sorting_column = self.SALE_DATE_COLUMN
        self.__sorting_order = Qt.DescendingOrder

        self.set_up_gui()

    def set_up_gui(self):
        loadUi(resource_path('view/ui/product_sale_management.ui'), self)
        self.__setup_tool_bar()
        self.__set_table_format()
        self.__wire_up_connections()
        self.edit_sale_button.setDisabled(True)
        self.undo_sale_button.setDisabled(True)
        self.disable_delete_filter_button(True)
        self.selected_quantity_label.hide()

    def __setup_tool_bar(self):
        self.__define_tool_bar_buttons()
        self.tool_bar = QToolBar()
        self.tool_bar_frame.setLayout(QHBoxLayout())
        self.tool_bar_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.tool_bar_frame.layout().setMenuBar(self.tool_bar)

        self.tool_bar.addWidget(self.back_button)
        self.tool_bar.addSeparator()
        self.tool_bar.addWidget(self.sell_button)
        self.tool_bar.addWidget(self.undo_sale_button)
        self.tool_bar.addWidget(self.edit_sale_button)
        self.tool_bar.addSeparator()
        self.tool_bar.addWidget(self.filter_button)
        self.tool_bar.addWidget(self.delete_filter_button)

    def __define_tool_bar_buttons(self):
        self.back_button = ToolButtonWithTextAndIcon('Atrás')
        self.back_button.set_icon(QPixmap(resource_path('view/ui/images/back.png')))

        self.sell_button = ToolButtonWithTextAndIcon('Vender')
        self.sell_button.set_icon(QPixmap(resource_path('view/ui/images/make_sale.png')))

        self.undo_sale_button = ToolButtonWithTextAndIcon('Deshacer')
        self.undo_sale_button.set_icon(QPixmap(resource_path('view/ui/images/undo_sale.png')))

        self.edit_sale_button = ToolButtonWithTextAndIcon('Editar')
        self.edit_sale_button.set_icon(QPixmap(resource_path('view/ui/images/edit.png')))

        self.filter_button = ToolButtonWithTextAndIcon('Filtrar')
        self.filter_button.set_icon(QPixmap(resource_path('view/ui/images/filter.png')))

        self.delete_filter_button = ToolButtonWithTextAndIcon('Quitar filtro')
        self.delete_filter_button.set_icon(QPixmap(resource_path('view/ui/images/delete_filter.png')))

    def __set_table_format(self):
        self.sale_table.setColumnCount(5)
        self.sale_table.setHorizontalHeaderLabels([
            'Id. Venta',
            'Pago',
            'Costo del producto',
            'Ganancia',
            'Fecha'
        ])
        self.sale_table.resizeColumnsToContents()
        self.sale_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.sale_table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        self.sale_table.horizontalHeader().setSectionsClickable(True)

    def __wire_up_connections(self):
        self.back_button.clicked.connect(self.__presenter.close_presenter)
        self.sell_button.clicked.connect(self.__presenter.open_make_sale_presenter)
        self.undo_sale_button.clicked.connect(self.__presenter.undo_selected_sales)
        self.edit_sale_button.clicked.connect(self.__presenter.open_presenter_to_edit_sale)
        self.sale_table.itemSelectionChanged.connect(self.__disable_buttons_depending_on_table_selection)
        self.sale_table.itemDoubleClicked.connect(self.__presenter.open_presenter_to_edit_sale)
        self.sale_table.itemSelectionChanged.connect(self.__set_selected_row_quantity_on_label)
        self.filter_button.clicked.connect(self.__presenter.open_filter_presenter)
        self.delete_filter_button.clicked.connect(self.__presenter.execute_thread_to_delete_applied_filter)
        self.sale_table.horizontalHeader().sectionClicked.connect(self.__change_sorting_configuration)
        self.sale_table.horizontalHeader().sectionClicked.connect(self.sort_table_rows)

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

    def __set_selected_row_quantity_on_label(self):
        selected_row_quantity = len(self.sale_table.selectionModel().selectedRows(self.SALE_ID_COLUMN))

        if selected_row_quantity == 1:
            self.selected_quantity_label.show()
            self.selected_quantity_label.setText('1 seleccionada')
        elif selected_row_quantity > 1:
            self.selected_quantity_label.show()
            self.selected_quantity_label.setText(f'{selected_row_quantity} seleccionadas')
        else:
            self.selected_quantity_label.setText('')

    def __change_sorting_configuration(self, clicked_header_section: int):
        if clicked_header_section == self.__sorting_column:
            self.__sorting_order = (Qt.AscendingOrder if self.__sorting_order == Qt.DescendingOrder
                                    else Qt.DescendingOrder)
        else:
            self.__sorting_column = clicked_header_section
            self.__sorting_order = Qt.AscendingOrder

    def sort_table_rows(self):
        horizontal_header = self.sale_table.horizontalHeader()
        horizontal_header.setSortIndicator(self.__sorting_column, self.__sorting_order)
        horizontal_header.setSortIndicatorShown(True)
        self.sale_table.sortItems(self.__sorting_column, self.__sorting_order)

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
        if column in [self.PAYMENT_COLUMN, self.COST_COLUMN, self.PROFIT_COLUMN]:
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
        self.quantity_value_label.setText(f'Cantidad Disponible: <b>{quantity}</b>')

    def ask_user_to_confirm_undo_sales(self) -> bool:
        quantity = self.__get_selected_sale_quantity()
        sale_word = self.__get_singular_or_plural_sale_word()

        message_box = QMessageBox(self.window())
        message_box.setIcon(QMessageBox.Question)
        message_box.setText(
            '¿Seguro que desea deshacer {} {}?\n\n'.format(quantity, sale_word) +
            'Esto se repondrá en la cantidad disponible del producto.'
            )
        message_box.setWindowTitle('Blue POS - Deshacer {}'.format(sale_word))

        undo_button = QPushButton(f'Deshacer {sale_word}')
        undo_button.setObjectName('dialog_delete_button')
        undo_button.setCursor(Qt.PointingHandCursor)
        message_box.addButton(undo_button, QMessageBox.AcceptRole)

        cancel_button = QPushButton('Cancelar')
        cancel_button.setCursor(Qt.PointingHandCursor)
        message_box.addButton(cancel_button, QMessageBox.NoRole)

        pressed_button = message_box.exec()
        return message_box.clickedButton() == undo_button

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

    def set_product_name(self, product_name: str):
        self.product_name_label.setText(f'Ventas de <b>{product_name}</b>')
