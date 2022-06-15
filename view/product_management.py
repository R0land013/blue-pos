from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class ProductManagementView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        loadUi('./view/ui/product_management.ui', self)
        self.__wire_up_gui_connections()

    def __wire_up_gui_connections(self):
        self.back_button.clicked.connect(self.__presenter.return_to_main)
