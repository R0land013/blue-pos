from datetime import date

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class CustomSaleReportView(QFrame):

    SALE_ID_REPORT_COLUMN = 'Id. de Venta'
    PAID_REPORT_COLUMN = 'Pagado'
    PROFIT_REPORT_COLUMN = 'Ganancia'
    SALE_DATE_REPORT_COLUMN = 'Fecha'

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/custom_sale_report.ui', self)
        self.__setup_date_edit()
        self.__setup_order_by_combo_box()
        self.__wire_up_gui_connections()

        self.state_bar_label.hide()

    def __setup_date_edit(self):
        self.initial_date_edit.setDate(QDate.currentDate())
        self.final_date_edit.setDate(QDate.currentDate())
        self.initial_date_edit.setMaximumDate(QDate.currentDate())
        self.final_date_edit.setMaximumDate(QDate.currentDate())
        self.initial_date_edit.lineEdit().setReadOnly(True)
        self.final_date_edit.lineEdit().setReadOnly(True)
        self.final_date_edit.dateChanged.connect(
            lambda: self.initial_date_edit.setMaximumDate(self.final_date_edit.date())
        )

    def __setup_order_by_combo_box(self):
        report_columns = [
            self.SALE_ID_REPORT_COLUMN,
            self.PAID_REPORT_COLUMN,
            self.PROFIT_REPORT_COLUMN,
            self.SALE_DATE_REPORT_COLUMN
        ]
        self.order_by_combo_box.addItems(report_columns)

    def __wire_up_gui_connections(self):
        self.back_button.clicked.connect(self.__presenter.close_presenter)
        self.create_report_button.clicked.connect(self.__presenter.open_custom_report_visualizer_presenter)

    def get_report_name(self) -> str:
        return self.name_line_edit.text().lstrip().strip()

    def get_report_description(self) -> str:
        return self.description_plain_text_edit.document().toRawText().lstrip().rstrip()

    def get_initial_date(self) -> date:
        qdate: QDate = self.initial_date_edit.date()
        return date(day=qdate.day(),
                    month=qdate.month(),
                    year=qdate.year())

    def get_final_date(self) -> date:
        qdate: QDate = self.final_date_edit.date()
        return date(day=qdate.day(),
                    month=qdate.month(),
                    year=qdate.year())

    def get_order_by_report_column(self) -> str:
        return self.order_by_combo_box.currentText()

    def is_ascending_order(self) -> bool:
        if self.ascending_radio_button.isChecked():
            return True
        return False
