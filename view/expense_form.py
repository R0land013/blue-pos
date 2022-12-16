from datetime import date

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QFrame, QMessageBox
from PyQt5.uic import loadUi


class ExpenseFormView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/expense_form.ui', self)
        self.__setup_date_edit()
        self.__setup_gui_connections()

    def __setup_date_edit(self):
        self.date_edit.setMaximumDate(QDate.currentDate())
        self.date_edit.setDate(QDate.currentDate())

    def __setup_gui_connections(self):
        self.cancel_button.clicked.connect(self.__presenter.close_presenter)
        self.save_button.clicked.connect(self.__presenter.execute_thread_to_save_expense)

    def hide_id_labels(self, hide: bool):
        if hide:
            self.id_label.hide()
            self.id_value_label.hide()
        else:
            self.id_label.show()
            self.id_value_label.show()

    def set_status_bar_message(self, message: str):
        self.status_bar_label.setText(message)

    def set_expense_id(self, id_value: int):
        self.id_value_label.setText(str(id_value))

    def get_expense_name(self) -> str:
        return self.name_line_edit.text().lstrip().rstrip()

    def set_expense_name(self, name: str):
        self.name_line_edit.setText(name)

    def get_expense_description(self) -> str:
        return self.description_plain_text_edit.toPlainText().lstrip().rstrip()

    def set_expense_description(self, description: str):
        self.description_plain_text_edit.setPlainText(description)

    def get_spent_money(self) -> str:
        return self.spent_money_spin_box.cleanText().split()[0]

    def set_spent_money(self, money: float):
        self.spent_money_spin_box.setValue(money)

    def get_date(self) -> date:
        qdate = self.date_edit.date()
        return date(day=qdate.day(),
                    month=qdate.month(),
                    year=qdate.year())

    def set_date(self, a_date: date):
        self.date_edit.setDate(QDate(a_date.year, a_date.month, a_date.day))

    def disable_all_gui(self, disable: bool):
        self.main_content_frame.setDisabled(disable)
        self.save_button.setDisabled(disable)
        self.cancel_button.setDisabled(disable)

    def show_dialog_error_message(self, message: str):
        QMessageBox.critical(self.window(), 'Error', message)