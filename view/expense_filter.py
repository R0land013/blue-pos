from PyQt5.QtWidgets import QFrame
from qtpy.uic import loadUi


class ExpenseFilterView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/expense_filter.ui', self)
        self.__setup_gui_connections()

    def __setup_gui_connections(self):
        self.cancel_button.clicked.connect(self.__presenter.close_presenter)