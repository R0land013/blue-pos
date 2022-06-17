from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class ProductView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        loadUi('./view/ui/product_form.ui', self)
        self.__wire_up_gui_connections()

    def __wire_up_gui_connections(self):
        self.save_button.clicked.connect(self.__presenter.save_product)
        self.cancel_button.clicked.connect(self.__presenter.go_back)

    def set_id_labels_invisible(self, invisible: bool):
        if invisible:
            self.id_label.hide()
            self.id_value_label.hide()
        else:
            self.id_label.show()
            self.id_value_label.show()

    def get_name(self) -> str:
        return self.name_line_edit.text()

    def get_description(self) -> str:
        return self.description_text_edit.document().toRawText()

    def get_price(self) -> str:
        return self.price_spin_box.cleanText()

    def get_profit(self) -> str:
        return self.profit_spin_box.cleanText()

    def get_quantity(self) -> int:
        return self.quantity_spin_box.value()
