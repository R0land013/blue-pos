from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QToolBar, QHBoxLayout, QToolButton, QTableWidget, QTableWidgetItem
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

        self.__setup_gui_connections()

    def __set_up_tool_bar(self):
        self.set_up_tool_buttons()
        self.tool_bar = QToolBar()
        self.tool_bar_frame.setLayout(QHBoxLayout())
        self.tool_bar_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.tool_bar_frame.layout().setMenuBar(self.tool_bar)

        self.tool_bar.addWidget(self.back_button)
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

        self.delete_button = QToolButton()
        self.delete_button.setIcon(QIcon('./view/ui/images/delete.png'))
        self.delete_button.setToolTip('Eliminar gasto')

        self.filter_button = QToolButton()
        self.filter_button.setIcon(QIcon('./view/ui/images/filter.png'))
        self.filter_button.setToolTip('Filtrar gastos')

        self.delete_filter_button = QToolButton()
        self.delete_filter_button.setIcon(QIcon('./view/ui/images/delete_filter.png'))
        self.delete_filter_button.setToolTip('Quitar filtro')

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

    def __setup_gui_connections(self):
        self.back_button.clicked.connect(self.__presenter.close_presenter)

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
