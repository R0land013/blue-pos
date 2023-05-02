from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi
from datetime import date
from util.resources_path import resource_path


class SaleFilterView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__set_up_gui()

    def __set_up_gui(self):
        loadUi(resource_path('view/ui/sale_filter.ui'), self)
        self.__setup_date_fields()
        self._wire_up_gui_connections()

    def __setup_date_fields(self):
        self.initial_date_edit.setDate(QDate.currentDate())
        self.final_date_edit.setDate(QDate.currentDate())

        self.final_date_edit.setMaximumDate(QDate.currentDate())
        self.initial_date_edit.setMaximumDate(QDate.currentDate())

        self.final_date_edit.dateChanged.connect(
            lambda new_date: self.initial_date_edit.setMaximumDate(new_date))
        self.final_sale_date_check_box.stateChanged.connect(
            self.__set_initial_maximum_date_to_today_if_final_date_edit_is_unchecked
        )

    def __set_initial_maximum_date_to_today_if_final_date_edit_is_unchecked(self, state):
        if state == Qt.Unchecked:
            self.initial_date_edit.setMaximumDate(QDate.currentDate())
        else:
            self.initial_date_edit.setMaximumDate(self.final_date_edit.date())

    def __set_initial_date_edit_maximum_date(self, new_date: QDate = None):
        self.initial_date_edit.setMaximumDate(new_date)

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

    def set_initial_date(self, initial_date: date):
        if initial_date is None: return
        
        self.initial_date_edit.setDate(QDate(
            initial_date.year,
            initial_date.month,
            initial_date.day
        ))

    def get_final_date(self) -> date:
        if not self.final_sale_date_check_box.isChecked():
            return None

        q_date = self.final_date_edit.date()
        return date(
            day=q_date.day(),
            month=q_date.month(),
            year=q_date.year()
        )
    
    def set_final_date(self, final_date: date):
        if final_date is None: return
        
        self.final_date_edit.setDate(QDate(
            final_date.year,
            final_date.month,
            final_date.day
        ))

    def set_initial_date_check_box_checked(self, checked: bool):
        if checked:
            self.initial_sale_date_check_box.setCheckState(Qt.Checked)
        else:
            self.initial_sale_date_check_box.setCheckState(Qt.Unchecked)
    
    def set_final_date_check_box_checked(self, checked: bool):
        if checked:
            self.final_sale_date_check_box.setCheckState(Qt.Checked)
        else:
            self.final_sale_date_check_box.setCheckState(Qt.Unchecked)