from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QSize, QPropertyAnimation, QPoint, QSequentialAnimationGroup, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QPaintEvent
from PyQt5.QtWidgets import QFrame, QApplication
from PyQt5.uic import loadUi

from view.util.animations import GoForwardAndReturnAnimation


class MainView(QFrame):

    clicked_on_next_label = pyqtSignal()
    clicked_on_previous_label = pyqtSignal()

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter
        self.__next_label_animation = None
        self.__previous_label_animation = None

        self.__set_up_gui()

    def __set_up_gui(self):
        loadUi('./view/ui/main.ui', self)
        self.__set_available_mouse_tracking()
        self.wire_up_gui_connections()

        self.previous_label.hide()  # Para que la navegación hacia la izquierda no aparezca

    def __set_available_mouse_tracking(self):
        self.setMouseTracking(True)
        self.next_label.setMouseTracking(True)
        self.previous_label.setMouseTracking(True)
        self.stacked_widget.setMouseTracking(True)

    def wire_up_gui_connections(self):
        self.product_management_button.clicked.connect(self.__presenter.open_product_management)
        self.day_report_button.clicked.connect(self.__presenter.open_day_sale_report_presenter)
        self.month_report_button.clicked.connect(self.__presenter.open_month_sale_report_presenter)
        self.year_report_button.clicked.connect(self.__presenter.open_year_sale_report_presenter)
        self.week_report_button.clicked.connect(self.__presenter.open_week_sale_report_presenter)
        self.custom_report_button.clicked.connect(self.__presenter.open_custom_sale_report_presenter)
        self.clicked_on_next_label.connect(self.__show_reports_widget)
        self.clicked_on_previous_label.connect(self.__show_management_widget)

    def __show_reports_widget(self):
        self.next_label.hide()
        self.previous_label.show()
        self.stacked_widget.setCurrentWidget(self.reports_widget)

    def __show_management_widget(self):
        self.previous_label.hide()
        self.next_label.show()
        self.stacked_widget.setCurrentWidget(self.management_widget)

    def mouseMoveEvent(self, event: QMouseEvent):
        self.__create_animations()
        self.__start_next_label_animation_if_mouse_is_hovering()
        self.__start_previous_label_animation_if_mouse_is_hovering()

    def __create_animations(self):
        if self.__next_label_animation is None:
            self.__next_label_animation = GoForwardAndReturnAnimation(
                self.next_label, b'pos', 30, GoForwardAndReturnAnimation.RIGHT_DIRECTION)
            self.__next_label_animation.finished.connect(
                self.__start_next_label_animation_if_mouse_is_hovering
            )

        if self.__previous_label_animation is None:
            self.__previous_label_animation = GoForwardAndReturnAnimation(
                self.previous_label, b'pos', 30, GoForwardAndReturnAnimation.LEFT_DIRECTION
            )
            self.__previous_label_animation.finished.connect(
                self.__start_previous_label_animation_if_mouse_is_hovering)

    def __start_next_label_animation_if_mouse_is_hovering(self):
        if self.next_label.underMouse() and (
                self.__next_label_animation.state() == QPropertyAnimation.Stopped):
            self.__next_label_animation.start()

    def __start_previous_label_animation_if_mouse_is_hovering(self):
        if self.previous_label.underMouse() and (
                self.__previous_label_animation.state() == QPropertyAnimation.Stopped):
            self.__previous_label_animation.start()

    def mouseReleaseEvent(self, mouse_event: QMouseEvent):
        if self.next_label.underMouse():
            self.clicked_on_next_label.emit()
        elif self.previous_label.underMouse():
            self.clicked_on_previous_label.emit()
