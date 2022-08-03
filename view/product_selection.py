from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class ProductSelectionView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/product_selection.ui', self)

        self.__wire_up_gui_connections()

    def __wire_up_gui_connections(self):
        self.cancel_button.clicked.connect(self.__presenter.cancel_selection_and_close_presenter)
