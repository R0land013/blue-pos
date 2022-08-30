from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class ExpensesVisualizationView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/expenses_visualization.ui', self)
        self.__setup_gui_connections()

    def __setup_gui_connections(self):
        self.close_button.clicked.connect(self.__presenter.close_presenter)