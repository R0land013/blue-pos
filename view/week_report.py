from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QFrame, QHBoxLayout
from PyQt5.uic import loadUi

from view.util.week_selector import QWeekCalendarSelectorWidget


class WeekSaleReportView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/week_sale_report.ui', self)
        self.__setup_week_calendar_selector()

        self.__wire_up_gui_connections()

    def __setup_week_calendar_selector(self):
        self.__week_calendar_selector = QWeekCalendarSelectorWidget()
        self.__week_calendar_selector.setSelectedDate(QDate.currentDate())
        self.calendar_frame.setLayout(QHBoxLayout())
        self.calendar_frame.layout().addWidget(self.__week_calendar_selector)

    def __wire_up_gui_connections(self):
        self.back_button.clicked.connect(self.__presenter.close_presenter)
