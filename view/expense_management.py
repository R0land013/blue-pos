from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QToolBar, QHBoxLayout, QToolButton, QTableWidget, QTableWidgetItem, QMessageBox
from qtpy.uic import loadUi

from view.util.table_columns import QCUPMoneyTableItem, QIntegerTableItem


class ExpenseManagementView(QFrame):

    ID_COLUMN = 0
    NAME_COLUMN = 1
    SPENT_MONEY_COLUMN = 2
    DATE_COLUMN = 3

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/expense_management.ui', self)
        self.__set_up_tool_bar()
        self.__setup_table()
        self.__sorting_column = self.DATE_COLUMN
        self.__sorting_order = Qt.DescendingOrder

        self.__setup_gui_connections()

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
        self.tool_bar.addWidget(self.filter_button)
        self.tool_bar.addWidget(self.delete_filter_button)

    def set_up_tool_buttons(self):
        self.back_button = QToolButton()
        self.back_button.setIcon(QIcon('./view/ui/images/back.png'))
        self.back_button.setToolTip('Regresar')

        self.new_button = QToolButton()
        self.new_button.setIcon(QIcon('./view/ui/images/new.png'))
        self.new_button.setToolTip('Nuevo gasto')

        self.edit_button = QToolButton()
        self.edit_button.setIcon(QIcon('./view/ui/images/edit.png'))
        self.edit_button.setToolTip('Editar gasto')
        self.edit_button.setDisabled(True)

        self.delete_button = QToolButton()
        self.delete_button.setIcon(QIcon('./view/ui/images/delete.png'))
        self.delete_button.setToolTip('Eliminar gasto')
        self.delete_button.setDisabled(True)

        self.filter_button = QToolButton()
        self.filter_button.setIcon(QIcon('./view/ui/images/filter.png'))
        self.filter_button.setToolTip('Filtrar gastos')

        self.delete_filter_button = QToolButton()
        self.delete_filter_button.setIcon(QIcon('./view/ui/images/delete_filter.png'))
        self.delete_filter_button.setToolTip('Quitar filtro')
        self.delete_filter_button.setDisabled(True)

    def __setup_table(self):
        self.expense_table.setColumnCount(4)
        self.expense_table.setHorizontalHeaderLabels([
            'Id.',
            'Nombre',
            'Dinero Gastado',
            'Fecha'
        ])
        self.expense_table.resizeColumnsToContents()
        self.expense_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.expense_table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        self.expense_table.horizontalHeader().setSectionsClickable(True)

    def __setup_gui_connections(self):
        self.back_button.clicked.connect(self.__presenter.close_presenter)
        self.new_button.clicked.connect(
            self.__presenter.open_expense_form_presenter_to_add_new_expense)
        self.edit_button.clicked.connect(self.__presenter.open_expense_form_presenter_to_update_expense)
        self.expense_table.itemSelectionChanged.connect(
            self.__disable_edit_and_delete_buttons_depending_on_row_selection)
        self.expense_table.itemDoubleClicked.connect(
            self.__presenter.open_expense_form_presenter_to_update_expense)
        self.delete_button.clicked.connect(self.__presenter.execute_thread_to_delete_selected_expenses)
        self.filter_button.clicked.connect(self.__presenter.open_expense_filter_presenter)
        self.delete_filter_button.clicked.connect(
            self.__presenter.execute_thread_to_delete_applied_filter)
        self.expense_table.horizontalHeader().sectionClicked.connect(self.__change_sorting_configuration)
        self.expense_table.horizontalHeader().sectionClicked.connect(self.sort_table_rows)

    def __disable_edit_and_delete_buttons_depending_on_row_selection(self):
        selected_row_quantity = len(self.expense_table.selectionModel().selectedRows(self.ID_COLUMN))

        if selected_row_quantity == 1:
            self.edit_button.setDisabled(False)
            self.delete_button.setDisabled(False)
        elif selected_row_quantity >= 1:
            self.edit_button.setDisabled(True)
            self.delete_button.setDisabled(False)
        else:
            self.edit_button.setDisabled(True)
            self.delete_button.setDisabled(True)

    def __change_sorting_configuration(self, clicked_header_section: int):
        if clicked_header_section == self.__sorting_column:
            self.__sorting_order = (Qt.AscendingOrder if self.__sorting_order == Qt.DescendingOrder
                                    else Qt.DescendingOrder)
        else:
            self.__sorting_column = clicked_header_section
            self.__sorting_order = Qt.AscendingOrder

    def sort_table_rows(self):
        horizontal_header = self.expense_table.horizontalHeader()
        horizontal_header.setSortIndicator(self.__sorting_column, self.__sorting_order)
        horizontal_header.setSortIndicatorShown(True)
        self.expense_table.sortItems(self.__sorting_column, self.__sorting_order)

    def set_status_bar_message(self, message: str):
        self.state_bar_label.setText(message)

    def disable_all_gui(self, disable: bool):
        self.main_content_frame.setDisabled(disable)

    def add_empty_row_at_the_end_of_table(self):
        new_row_index = self.expense_table.rowCount()
        self.expense_table.insertRow(new_row_index)

    def get_last_row_index(self) -> int:
        return self.expense_table.rowCount() - 1

    def set_cell_in_table(self, row: int, column: int, data):

        item = QTableWidgetItem(str(data))
        if column == self.SPENT_MONEY_COLUMN:
            item = QCUPMoneyTableItem(str(data))
        elif column == self.ID_COLUMN:
            item = QIntegerTableItem(str(data))

        self.expense_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.expense_table.setItem(row, column, item)

    def resize_table_columns_to_contents(self):
        self.expense_table.resizeColumnsToContents()

    def get_selected_row_index(self) -> int:
        return self.expense_table.currentRow()

    def get_all_selected_expense_ids(self) -> list:
        ids = []
        model_indexes = self.expense_table.selectionModel().selectedRows(self.ID_COLUMN)
        for a_model_index in model_indexes:
            row = a_model_index.row()
            expense_id = int(self.expense_table.item(row, self.ID_COLUMN).text())
            ids.append(expense_id)
        return ids

    def delete_selected_rows_from_table(self):
        model_indexes = self.expense_table.selectionModel().selectedRows(self.ID_COLUMN)
        selected_row_quantity = len(model_indexes)

        while selected_row_quantity != 0:
            a_row = model_indexes[0].row()
            self.expense_table.removeRow(a_row)

            model_indexes = self.expense_table.selectionModel().selectedRows(self.ID_COLUMN)
            selected_row_quantity = len(model_indexes)

        self.expense_table.clearSelection()
        self.__disable_edit_and_delete_buttons_depending_on_row_selection()

    def ask_user_to_confirm_deleting_expenses(self) -> bool:
        message_box = self.__construct_message_box()
        pressed_button = message_box.exec()
        return pressed_button == QMessageBox.StandardButton.Ok

    def __construct_message_box(self) -> QMessageBox:
        quantity = self.__get_selected_expenses_quantity()
        expense_word = self.__get_singular_or_plural_expense_word()

        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Question)
        message_box.setWindowTitle('Blue POS - Eliminar {}'.format(expense_word))
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        message_box.setText('¿Seguro que desea eliminar {} {}?'.format(quantity, expense_word))
        return message_box

    def __get_selected_expenses_quantity(self) -> int:
        return len(self.expense_table.selectionModel().selectedRows(self.ID_COLUMN))

    def __get_singular_or_plural_expense_word(self):
        expense_selected_quantity = self.__get_selected_expenses_quantity()
        if expense_selected_quantity == 1:
            return 'gasto'
        return 'gastos'

    def set_applied_filter_message(self, applied: bool):
        if applied:
            self.filter_state_label.setText('Filtro aplicado')
        else:
            self.filter_state_label.setText('Sin filtros')

    def set_delete_filter_disabled(self, disabled: bool):
        self.delete_filter_button.setDisabled(disabled)

    def clean_table(self):
        while self.expense_table.rowCount() > 0:
            self.expense_table.removeRow(0)
