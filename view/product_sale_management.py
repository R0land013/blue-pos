from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class ProductSaleManagementView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        loadUi('./view/ui/product_sale_management.ui', self)
        self.__wire_up_connections()

    def __wire_up_connections(self):
        self.back_button.clicked.connect(self.__presenter.close_presenter)
