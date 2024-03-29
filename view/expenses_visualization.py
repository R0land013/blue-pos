from datetime import date

from PyQt5.QtCore import QItemSelection, Qt
from PyQt5.QtWidgets import QFrame, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi
from money import Money
from view.util.table_columns import QCUPMoneyTableItem, QIntegerTableItem
from util.resources_path import resource_path


class ExpensesVisualizationView(QFrame):

    ID_COLUMN = 0
    NAME_COLUMN = 1
    SPENT_MONEY_COLUMN = 2
    DATE_COLUMN = 3

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter
        self.__sorting_column = self.DATE_COLUMN
        self.__sorting_order = Qt.AscendingOrder

        self.__setup_gui()

    def __setup_gui(self):
        loadUi(resource_path('view/ui/expenses_visualization.ui'), self)
        self.__setup_table()

        self.__setup_gui_connections()

    def __setup_table(self):
        self.expense_table.setColumnCount(4)
        self.expense_table.setHorizontalHeaderLabels([
            'Id. Gasto',
            'Nombre',
            'Dinero gastado',
            'Fecha'
        ])
        self.expense_table.resizeColumnsToContents()
        self.expense_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.expense_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.expense_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.expense_table.horizontalHeader().setSectionsClickable(True)

    def __setup_gui_connections(self):
        self.close_button.clicked.connect(self.__presenter.close_presenter)
        self.expense_table.itemSelectionChanged.connect(self.__set_expense_description_if_there_is_row_selected)
        self.expense_table.horizontalHeader().sectionClicked.connect(self.__change_sorting_configuration)
        self.expense_table.horizontalHeader().sectionClicked.connect(self.sort_table_rows)

    def __set_expense_description_if_there_is_row_selected(self):
        if self.expense_table.currentRow() != -1:
            self.__presenter.set_expense_description()

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

    def disable_view(self, disable: bool):
        self.main_content_frame.setDisabled(disable)
        self.close_button.setDisabled(disable)

    def set_status_bar_message(self, message: str):
        self.state_bar_label.setText(message)

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

    def set_date_range_for_message(self, initial_date: date, final_date: date):
        message = 'Gastos desde <b>{}-{}-{}</b> hasta <b>{}-{}-{}</b>'.format(
            initial_date.day, initial_date.month, initial_date.year,
            final_date.day, final_date.month, final_date.year
        )
        if initial_date == final_date:
            message = f'Gastos de <b>{initial_date.day}-{initial_date.month}-{initial_date.year}</b>'
        self.expense_date_range_label.setText(message)

    def set_total_expense(self, total_expense: Money):
        self.total_expense_label.setText('-{} CUP'.format(total_expense.amount))

    def set_description(self, description: str):
        self.description_plain_text_edit.setPlainText(description)

    def set_first_row_selected(self):
        if self.expense_table.rowCount() > 0:
            self.expense_table.selectionModel().clear()
            self.expense_table.selectRow(0)

    def get_selected_expense_id(self) -> int:
        if self.expense_table.currentRow() != -1:
            row = self.expense_table.currentRow()
            return int(self.expense_table.item(row, self.ID_COLUMN).text())
        return -1