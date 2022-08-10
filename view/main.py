from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QSize, QPropertyAnimation, QPoint, QSequentialAnimationGroup, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QPaintEvent
from PyQt5.QtWidgets import QFrame, QApplication
from PyQt5.uic import loadUi


class MainView(QFrame):

    clicked_on_next_label = pyqtSignal()
    clicked_on_previous_label = pyqtSignal()

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__set_up_gui()

    def __set_up_gui(self):
        loadUi('./view/ui/main.ui', self)
        self.__set_available_mouse_tracking()
        self.__setup_next_navigation_label_animations()
        self.__setup_previous_navigation_label_animations()
        self.wire_up_gui_connections()

        self.previous_label.hide()  # Para que la navegación hacia la izquierda no aparezca

    def __set_available_mouse_tracking(self):
        self.setMouseTracking(True)
        self.next_label.setMouseTracking(True)
        self.previous_label.setMouseTracking(True)
        self.stacked_widget.setMouseTracking(True)

    def __setup_next_navigation_label_animations(self):
        self.next_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.__next_label_animation = QSequentialAnimationGroup()
        go_to_right = QPropertyAnimation(self.next_label, b'pos')
        go_to_right.setDuration(500)
        go_to_left = QPropertyAnimation(self.next_label, b'pos')
        go_to_left.setDuration(500)
        self.__next_label_animation.addAnimation(go_to_right)
        self.__next_label_animation.addAnimation(go_to_left)
        self.__next_label_animation.finished.connect(self.__restart_next_label_animation_if_cursor_is_still_hovering)

    def __restart_next_label_animation_if_cursor_is_still_hovering(self):
        if self.next_label.underMouse() and (
                self.__next_label_animation.state() == QPropertyAnimation.Stopped):
            self.__next_label_animation.start()

    def __setup_previous_navigation_label_animations(self):
        self.previous_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.__previous_label_animation = QSequentialAnimationGroup()
        go_to_left = QPropertyAnimation(self.previous_label, b'pos')
        go_to_left.setDuration(500)
        go_to_right = QPropertyAnimation(self.previous_label, b'pos')
        go_to_right.setDuration(500)
        self.__previous_label_animation.addAnimation(go_to_left)
        self.__previous_label_animation.addAnimation(go_to_right)
        self.__previous_label_animation.finished.connect(
            self.__restart_previous_label_animation_if_cursor_is_still_hovering)

    def __restart_previous_label_animation_if_cursor_is_still_hovering(self):
        if self.previous_label.underMouse() and (
                self.__previous_label_animation.state() == QPropertyAnimation.Stopped):
            self.__previous_label_animation.start()

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
        self.__start_next_label_animation()
        self.__start_previous_label_animation()

    def __start_next_label_animation(self):
        if self.next_label.underMouse() and (
                self.__next_label_animation.state() == QPropertyAnimation.Stopped):
            go_to_right = self.__next_label_animation.animationAt(0)
            go_to_right.setStartValue(self.next_label.pos())
            go_to_right.setEndValue(self.next_label.pos() + QPoint(30, 0))

            go_to_left = self.__next_label_animation.animationAt(1)
            go_to_left.setStartValue(self.next_label.pos() + QPoint(30, 0))
            go_to_left.setEndValue(self.next_label.pos())
            self.__next_label_animation.start()

    def __start_previous_label_animation(self):
        if self.previous_label.underMouse() and (
                self.__previous_label_animation.state() == QPropertyAnimation.Stopped):
            go_to_left = self.__previous_label_animation.animationAt(0)
            go_to_left.setStartValue(self.previous_label.pos())
            go_to_left.setEndValue(self.previous_label.pos() - QPoint(30, 0))

            go_to_right = self.__previous_label_animation.animationAt(1)
            go_to_right.setStartValue(self.previous_label.pos() - QPoint(30, 0))
            go_to_right.setEndValue(self.previous_label.pos())
            self.__previous_label_animation.start()

    def mouseReleaseEvent(self, mouse_event: QMouseEvent):
        if self.next_label.underMouse():
            self.clicked_on_next_label.emit()
        elif self.previous_label.underMouse():
            self.clicked_on_previous_label.emit()
