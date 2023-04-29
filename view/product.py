from PyQt5.QtWidgets import QFrame, QMessageBox
from PyQt5.uic import loadUi
from model.util.monetary_types import CUPMoney
from model.entity.models import PRODUCT_DESCRIPTION_MAX_LENGTH, PRODUCT_NAME_MAX_LENGTH
from view.util.plain_text_edit import PlainTextEdit
from PyQt5.QtCore import Qt
from view.util.cup_spin_box import CUPSpinBox


class ProductView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.description_text_edit: PlainTextEdit = None
        self.price_spin_box: CUPSpinBox = None
        self.cost_spin_box: CUPSpinBox = None

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/product_form.ui', self)
        
        self.__setup_price_and_cost_spin_boxes()
        self.name_line_edit.setMaxLength(PRODUCT_NAME_MAX_LENGTH)
        self.__add_description_field()
        
        self.__wire_up_gui_connections()

    def __setup_price_and_cost_spin_boxes(self):
        self.price_spin_box = CUPSpinBox(minimum=0.010000, maximum=10000000.00, value=10.00)
        self.cost_spin_box = CUPSpinBox(minimum=0.000000, maximum=10000000, value=0.00)
        self.grid_form_frame.layout().addWidget(self.price_spin_box, 2, 1)
        self.grid_form_frame.layout().addWidget(self.cost_spin_box, 3, 1)
        self.price_spin_box.valueChanged.connect(self.__set_profit_label_depending_on_price_and_cost)
        self.cost_spin_box.valueChanged.connect(self.__set_profit_label_depending_on_price_and_cost)

    def __set_profit_label_depending_on_price_and_cost(self):
        price = CUPMoney(self.get_price())
        cost = CUPMoney(self.get_cost())
        profit = price - cost
        self.set_profit(float(profit.amount))
        if profit <= CUPMoney('0.00'):
            self.profit_value_label.setStyleSheet('color: red;')
        else:
            self.profit_value_label.setStyleSheet('color: black;')

    def __add_description_field(self):
        layout = self.description_frame.layout()
        self.description_text_edit = PlainTextEdit(self.description_frame)
        self.description_text_edit.set_maximum_length(PRODUCT_DESCRIPTION_MAX_LENGTH)
        self.description_text_edit.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        
        layout.addWidget(self.description_text_edit)

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
        return self.name_line_edit.text().strip()

    def set_name(self, name: str):
        self.name_line_edit.setText(name)

    def get_description(self) -> str:
        return self.description_text_edit.document().toRawText().strip()

    def set_description(self, description: str):
        self.description_text_edit.insertPlainText(description)

    def get_price(self) -> str:
        return self.price_spin_box.cleanText().split()[0]

    def set_price(self, price: float):
        self.price_spin_box.setValue(price)

    def get_cost(self) -> str:
        return self.cost_spin_box.cleanText().split()[0]

    def set_cost(self, cost: float):
        self.cost_spin_box.setValue(cost)

    def set_profit(self, amount: float):
        self.profit_value_label.setText('{} CUP'.format(str(amount)))

    def get_quantity(self) -> int:
        return self.quantity_spin_box.value()

    def set_quantity(self, quantity: str):
        self.quantity_spin_box.setValue(int(quantity))

    def show_error_message(self, message: str):
        QMessageBox.critical(self.window(), 'Error', message)

    def ask_user_to_confirm_no_profit_product_if_needed(self) -> bool:
        price = CUPMoney(self.get_price())
        cost = CUPMoney(self.get_cost())
        if cost < price:
            return True

        if cost > price:
            window_title = 'El producto generará pérdidas'
            detail_message = '¿Seguro que desea un producto que genera pérdidas?'
        elif cost == price:
            window_title = 'El producto no generará ganancias'
            detail_message = '¿Seguro que desea un producto que no genera ganancias?'

        pressed_button = QMessageBox.question(self.window(),
                                              window_title,
                                              detail_message,
                                              QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        if pressed_button == QMessageBox.StandardButton.Ok:
            return True
        return False
