from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QToolBar, QHBoxLayout, QToolButton
from qtpy.uic import loadUi


class ExpenseManagementView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/expense_management.ui', self)
        self.__set_up_tool_bar()

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

    def __setup_gui_connections(self):
        self.back_button.clicked.connect(self.__presenter.close_presenter)
