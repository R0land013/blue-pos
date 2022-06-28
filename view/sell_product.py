from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class MakeSaleView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        loadUi('./view/ui/make_sale_form.ui', self)
