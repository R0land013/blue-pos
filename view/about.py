from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class AboutView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/about.ui', self)
        self.__wire_up_connections()

    def __wire_up_connections(self):
        self.back_button.clicked.connect(self.__presenter.close_presenter)