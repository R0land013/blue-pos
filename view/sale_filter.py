from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class SaleFilterView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__set_up_gui()

    def __set_up_gui(self):
        loadUi('./view/ui/sale_filter.ui', self)
        self._wire_up_gui_connections()

    def _wire_up_gui_connections(self):
        self.cancel_button.clicked.connect(self.__presenter.close_presenter)
