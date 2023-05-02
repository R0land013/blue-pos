from datetime import date

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi
from util.resources_path import resource_path


class MakeSaleView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__set_up_gui()

    def __set_up_gui(self):
        loadUi(resource_path('view/ui/make_sale_form.ui'), self)
        self.__setup_date_edit()
        self.__wire_up_gui_connections()

    def __setup_date_edit(self):
        self.sale_date_edit.setDate(QDate.currentDate())
        self.sale_date_edit.setMaximumDate(QDate.currentDate())

    def __wire_up_gui_connections(self):
        self.sale_quantity_spin_box.valueChanged.connect(
            self.__presenter.set_sale_result_by_quantity)
        self.cancel_button.clicked.connect(
            self.__presenter.cancel_sale
        )
        self.confirm_button.clicked.connect(
            self.__presenter.make_sales_and_close_presenter
        )

    def set_limit_of_sales(self, available_quantity: int):
        self.sale_quantity_spin_box.setMinimum(1)
        self.sale_quantity_spin_box.setMaximum(available_quantity)

    def get_sale_quantity(self) -> int:
        return self.sale_quantity_spin_box.value()

    def get_sale_date(self) -> date:
        q_date = self.sale_date_edit.date()
        return date(
            day=q_date.day(),
            month=q_date.month(),
            year=q_date.year()
        )

    def set_money_to_pay(self, amount: str):
        self.money_to_pay_label.setText('{} CUP'.format(amount))

    def hide_status_bar(self, set_hidden: bool):
        if set_hidden:
            self.state_bar_label.hide()
        else:
            self.state_bar_label.show()

    def set_status_bar_message(self, message: str):
        self.state_bar_label.setText(message)

    def disable_all_view_except_status_bar(self, disabled: bool):
        self.main_content_frame.setDisabled(disabled)

