from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi
from datetime import date


class SaleFilterView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__set_up_gui()

    def __set_up_gui(self):
        loadUi('./view/ui/sale_filter.ui', self)
        self.__set_date_fields_to_today_date()
        self.__set_date_fields_limits()
        self._wire_up_gui_connections()

    def __set_date_fields_to_today_date(self):
        q_date = QDate()
        today = date.today()
        q_date.setDate(
            today.year,
            today.month,
            today.day
        )
        self.initial_date_edit.setDate(q_date)
        self.final_date_edit.setDate(q_date)

    def __set_date_fields_limits(self):
        self.initial_date_edit.setMaximumDate(QDate.currentDate())
        self.final_date_edit.setMaximumDate(QDate.currentDate())

    def _wire_up_gui_connections(self):
        self.cancel_button.clicked.connect(self.__presenter.close_presenter)
        self.__set_check_boxes_connections()
        self.filter_button.clicked.connect(self.__presenter.create_sale_filter_and_close)

    def __set_check_boxes_connections(self):
        self.initial_sale_date_check_box.stateChanged.connect(
            self.__change_initial_sale_date_availability)
        self.initial_sale_date_check_box.stateChanged.connect(
            self.__change_filter_button_availability
        )
        self.final_sale_date_check_box.stateChanged.connect(
            self.__change_final_sale_date_availability
        )
        self.final_sale_date_check_box.stateChanged.connect(
            self.__change_filter_button_availability
        )

    def __change_initial_sale_date_availability(self):
        self.initial_date_edit.setDisabled(
            not self.initial_sale_date_check_box.isChecked()
        )

    def __change_final_sale_date_availability(self):
        self.final_date_edit.setDisabled(
            not self.final_sale_date_check_box.isChecked()
        )

    def __change_filter_button_availability(self):
        if (self.initial_sale_date_check_box.isChecked() or
                self.final_sale_date_check_box.isChecked()):
            self.filter_button.setDisabled(False)
        else:
            self.filter_button.setDisabled(True)

    def get_initial_date(self) -> date:
        if not self.initial_sale_date_check_box.isChecked():
            return None

        q_date = self.initial_date_edit.date()
        return date(
            day=q_date.day(),
            month=q_date.month(),
            year=q_date.year()
        )

    def get_final_date(self) -> date:
        if not self.final_sale_date_check_box.isChecked():
            return None

        q_date = self.final_date_edit.date()
        return date(
            day=q_date.day(),
            month=q_date.month(),
            year=q_date.year()
        )
