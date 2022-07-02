from datetime import date

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class EditSaleView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.set_up_gui()

    def set_up_gui(self):
        loadUi('./view/ui/edit_sale_form.ui', self)
        self.wire_up_gui_connections()

    def wire_up_gui_connections(self):
        self.cancel_button.clicked.connect(self.__presenter.close_presenter)
        self.update_button.clicked.connect(self.__presenter.update_sale_and_close_presenter)

    def set_product_name(self, product_name: str):
        self.product_name_label.setText(product_name)

    def set_sale_id(self, sale_id: int):
        self.sale_id_label.setText(str(sale_id))

    def set_paid_money(self, paid_money: float):
        self.paid_money_spin_box.setValue(paid_money)

    def get_paid_money_as_str(self) -> str:
        """This returns the numeric part of a string like '10.55 CUP'. '10.55' would be returned."""
        return self.paid_money_spin_box.cleanText().split()[0]

    def set_profit_money(self, profit_money: float):
        self.profit_money_spin_box.setValue(profit_money)

    def get_profit_money_as_str(self) -> str:
        """This returns the numeric part of a string like '10.55 CUP'. '10.55' would be returned."""
        return self.profit_money_spin_box.cleanText().split()[0]

    def set_sale_date(self, sale_date: date):
        q_date = QDate()
        q_date.setDate(
            sale_date.year,
            sale_date.month,
            sale_date.day
        )
        self.sale_date_edit.setDate(q_date)

    def get_sale_date(self) -> date:
        q_date = self.sale_date_edit.date()
        return date(
            day=q_date.day(),
            month=q_date.month(),
            year=q_date.year()
        )

    def hide_status_bar(self, set_hidden: bool):
        if set_hidden:
            self.status_bar_label.hide()
        else:
            self.status_bar_label.show()

    def set_status_bar_message(self, message: str):
        self.status_bar_label.setText(message)
