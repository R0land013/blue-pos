from PyQt5.QtWidgets import QFrame, QMessageBox
from PyQt5.uic import loadUi


class ProductView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/product_form.ui', self)
        self.__setup_price_and_profit_spin_boxes()
        self.__wire_up_gui_connections()

    def __setup_price_and_profit_spin_boxes(self):
        self.profit_spin_box.setMaximum(self.price_spin_box.value())
        self.price_spin_box.valueChanged.connect(
            lambda value: self.profit_spin_box.setMaximum(value))

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

    def set_state_bar_invisible(self, invisible: bool):
        if invisible:
            self.state_bar_label.hide()
        else:
            self.state_bar_label.show()

    def set_state_bar_message(self, message: str):
        self.state_bar_label.setText(message)

    def set_disabled_view_except_state_bar(self, disabled: bool):
        self.main_content_frame.setDisabled(disabled)

    def set_product_id(self, product_id: int):
        self.id_value_label.setText(str(product_id))

    def get_name(self) -> str:
        return self.name_line_edit.text()

    def set_name(self, name: str):
        self.name_line_edit.setText(name)

    def get_description(self) -> str:
        return self.description_text_edit.document().toRawText()

    def set_description(self, description: str):
        self.description_text_edit.insertPlainText(description)

    def get_price(self) -> str:
        return self.price_spin_box.cleanText()

    def set_price(self, price: float):
        self.price_spin_box.setValue(price)

    def get_profit(self) -> str:
        return self.profit_spin_box.cleanText()

    def set_profit(self, profit: float):
        self.profit_spin_box.setValue(profit)

    def get_quantity(self) -> int:
        return self.quantity_spin_box.value()

    def set_quantity(self, quantity: str):
        self.quantity_spin_box.setValue(int(quantity))

    def show_error_message(self, message: str):
        QMessageBox.critical(self.window(), 'Error', message)
