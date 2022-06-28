from PyQt5.QtWidgets import QFrame, QTableWidget
from PyQt5.uic import loadUi


class ProductSaleManagementView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.set_up_gui()

    def set_up_gui(self):
        loadUi('./view/ui/product_sale_management.ui', self)
        self.__set_table_format()
        self.__wire_up_connections()

    def __wire_up_connections(self):
        self.back_button.clicked.connect(self.__presenter.close_presenter)

    def __set_table_format(self):
        self.sale_table.setColumnCount(4)
        self.sale_table.setHorizontalHeaderLabels([
            'Id. Venta',
            'Pago',
            'Ganancia',
            'Fecha'
        ])
        self.sale_table.resizeColumnsToContents()
        self.sale_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.sale_table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)