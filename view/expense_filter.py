from datetime import date

from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class ExpenseFilterView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/expense_filter.ui', self)
        self.__setup_date_fields()
        self.__setup_gui_connections()

    def __setup_date_fields(self):
        self.initial_date_edit.setMaximumDate(QDate.currentDate())
        self.initial_date_edit.setDate(QDate.currentDate())

        self.final_date_edit.setMaximumDate(QDate.currentDate())
        self.final_date_edit.setDate(QDate.currentDate())
        self.final_date_edit.dateChanged.connect(
            lambda new_max_date: self.initial_date_edit.setMaximumDate(new_max_date))
        self.final_date_check_box.stateChanged.connect(
            self.__set_maximum_date_on_initial_field_depending_on_final_field
        )

    def __set_maximum_date_on_initial_field_depending_on_final_field(self):
        if self.final_date_check_box.checkState() == Qt.Checked:
            final_date = self.final_date_edit.date()
            self.initial_date_edit.setMaximumDate(final_date)

        else:
            self.initial_date_edit.setMaximumDate(QDate.currentDate())

    def __setup_gui_connections(self):
        self.cancel_button.clicked.connect(self.__presenter.close_presenter)
        self.phrase_check_box.stateChanged.connect(self.__handle_phrase_field_availability)
        self.initial_date_check_box.stateChanged.connect(self.__handle_initial_date_field_availability)
        self.final_date_check_box.stateChanged.connect(self.__handle_final_date_field_availability)
        self.apply_filter_button.clicked.connect(
            self.__presenter.return_filter_to_caller_of_this_presenter)

    def __handle_phrase_field_availability(self, check_state):
        if check_state == Qt.Checked:
            self.phrase_line_edit.setDisabled(False)
        else:
            self.phrase_line_edit.setDisabled(True)

    def __handle_initial_date_field_availability(self, check_state):
        if check_state == Qt.Checked:
            self.initial_date_edit.setDisabled(False)
        else:
            self.initial_date_edit.setDisabled(True)

    def __handle_final_date_field_availability(self, check_state):
        if check_state == Qt.Checked:
            self.final_date_edit.setDisabled(False)
        else:
            self.final_date_edit.setDisabled(True)

    def set_phrase_check_box_checked(self, checked: bool):
        if checked:
            self.phrase_check_box.setCheckState(Qt.Checked)
        else:
            self.phrase_check_box.setCheckState(Qt.Unchecked)

    def set_initial_date_check_box_checked(self, checked: bool):
        if checked:
            self.initial_date_check_box.setCheckState(Qt.Checked)
        else:
            self.initial_date_check_box.setCheckState(Qt.Unchecked)

    def set_final_date_check_box_checked(self, checked: bool):
        if checked:
            self.final_date_check_box.setCheckState(Qt.Checked)
        else:
            self.final_date_check_box.setCheckState(Qt.Unchecked)

    def get_phrase(self) -> str:
        if self.phrase_check_box.checkState() == Qt.Unchecked:
            return None
        return self.phrase_line_edit.text().rstrip().lstrip()

    def set_phrase(self, phrase: str):
        self.phrase_line_edit.setText(phrase)

    def get_initial_date(self) -> date:
        if self.initial_date_check_box.checkState() == Qt.Unchecked:
            return None
        qdate = self.initial_date_edit.date()
        return date(
            day=qdate.day(),
            month=qdate.month(),
            year=qdate.year()
        )

    def set_initial_date(self, a_date: date):
        self.initial_date_edit.setDate(QDate(a_date.year, a_date.month, a_date.day))

    def get_final_date(self) -> date:
        if self.final_date_check_box.checkState() == Qt.Unchecked:
            return None
        qdate = self.final_date_edit.date()
        return date(
            day=qdate.day(),
            month=qdate.month(),
            year=qdate.year()
        )

    def set_final_date(self, a_date: date):
        self.final_date_edit.setDate(QDate(a_date.year, a_date.month, a_date.day))
