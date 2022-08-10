from datetime import date, timedelta
from PyQt5.QtGui import QPainter, QColor, QTextCharFormat, QPalette
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtCore import QDate, QRect, Qt, pyqtSignal


class QWeekCalendarSelectorWidget(QCalendarWidget):

    week_changed = pyqtSignal(QDate, QDate)

    def __init__(self):
        super().__init__()
        self.__first_date_of_week = None
        self.__last_date_of_week = None

        self.__HIGHLIGHTED_CALENDAR_FORMAT = QTextCharFormat()
        self.__HIGHLIGHTED_CALENDAR_FORMAT.setBackground(self.palette().brush(QPalette.Highlight))
        self.__HIGHLIGHTED_CALENDAR_FORMAT.setForeground(self.palette().color(QPalette.HighlightedText))
        self.__RESET_CALENDAR_FORMAT = QTextCharFormat()

        self.clicked.connect(self.__change_selected_week)
        self.selectionChanged.connect(self.__change_selected_week)
        self.__change_selected_week(self.selectedDate())

        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

    def __change_selected_week(self, qdate: QDate = None):
        # Si este método es llamado por la señal selectionChanged
        if qdate is None:
            qdate = self.selectedDate()

        self.__set_calendar_format(self.__RESET_CALENDAR_FORMAT)

        initial_date = self.__first_date_of_week
        final_date = self.__last_date_of_week

        self.__first_date_of_week = self.__get_first_qdate_of_week(qdate)
        self.__last_date_of_week = self.__get_last_qdate_of_week(qdate)

        self.__set_calendar_format(self.__HIGHLIGHTED_CALENDAR_FORMAT)
        self.__notify_listeners_if_week_is_changed(initial_date, final_date)

    def __get_first_qdate_of_week(self, qdate: QDate) -> QDate:
        py_date = self.__to_python_date(qdate)

        if py_date.weekday() > 0:
            first_week_py_date = py_date - timedelta(days=py_date.weekday())

            if self.__to_qdate(first_week_py_date) < self.minimumDate():
                return self.minimumDate()
            return self.__to_qdate(first_week_py_date)

        return qdate

    def __get_last_qdate_of_week(self, qdate: QDate) -> QDate:
        py_date = self.__to_python_date(qdate)

        if py_date.weekday() < 6:
            last_week_py_date = py_date + timedelta(days=6 - py_date.weekday())

            if self.__to_qdate(last_week_py_date) > self.maximumDate():
                return self.maximumDate()
            return self.__to_qdate(last_week_py_date)
        return qdate

    @staticmethod
    def __to_python_date(qdate: QDate) -> date:
        return date(day=qdate.day(), month=qdate.month(), year=qdate.year())

    @staticmethod
    def __to_qdate(py_date: date) -> QDate:
        return QDate(py_date.year, py_date.month, py_date.day)

    def setDateRange(self, minimum_date: QDate, maximum_date: QDate):
        super().setDateRange(minimum_date, maximum_date)
        self.__change_selected_week(self.selectedDate())

    def setMaximumDate(self, maximum_date: QDate):
        super().setMaximumDate(maximum_date)
        self.__change_selected_week(self.selectedDate())

    def setMinimumDate(self, minimum_date: QDate):
        super().setMinimumDate(minimum_date)
        self.__change_selected_week(self.selectedDate())

    def get_selected_date_range(self) -> tuple:
        """Returns a tuple containing two elements. The first is the first
        date of the week, and the second one the last date of the week."""
        return self.__first_date_of_week, self.__last_date_of_week

    def __set_calendar_format(self, a_format: QTextCharFormat):
        if self.__first_date_of_week and self.__last_date_of_week:
            initial_date = self.__first_date_of_week
            final_date = self.__last_date_of_week

            while initial_date <= final_date:
                self.setDateTextFormat(initial_date, a_format)
                initial_date = initial_date.addDays(1)

    def paintCell(self, painter: QPainter, rect: QRect, qdate: QDate):

        if self.__first_date_of_week <= qdate <= self.__last_date_of_week:
            self.__paint_selected_week_cell(painter, rect, qdate)
        else:
            super().paintCell(painter, rect, qdate)

    def __notify_listeners_if_week_is_changed(self, initial_date: QDate, final_date: QDate):
        if initial_date != self.__first_date_of_week and final_date != self.__last_date_of_week:
            self.week_changed.emit(self.__first_date_of_week, self.__last_date_of_week)

    @staticmethod
    def __paint_selected_week_cell(painter: QPainter, rect: QRect, qdate: QDate):
        painter.fillRect(rect, QColor(102, 178, 255))
        painter.save()
        painter.setPen(Qt.white)
        painter.drawText(rect, Qt.AlignCenter, str(qdate.day()))
        painter.restore()
