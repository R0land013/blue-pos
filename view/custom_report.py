from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class CustomSaleReportView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/custom_sale_report.ui', self)
        self.__wire_up_gui_connections()

    def __wire_up_gui_connections(self):
        self.back_button.clicked.connect(self.__presenter.close_presenter)
