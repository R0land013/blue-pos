from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QSize, QPropertyAnimation, QPoint, QSequentialAnimationGroup, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QPaintEvent
from PyQt5.QtWidgets import QFrame, QApplication
from PyQt5.uic import loadUi

from view.util.animations import GoForwardAndReturnAnimation


class MainView(QFrame):

    clicked_on_next_frame = pyqtSignal()
    clicked_on_previous_frame = pyqtSignal()
    clicked_on_about_label = pyqtSignal()

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter
        self.__next_frame_animation = None
        self.__previous_frame_animation = None

        self.__set_up_gui()
        self.__pages_of_stacked_widget = [
            self.statistics_widget,
            self.management_widget,
            self.reports_widget
        ]
        self.__selected_page_index = 1

    def __set_up_gui(self):
        loadUi('./view/ui/main.ui', self)
        self.wire_up_gui_connections()

    def wire_up_gui_connections(self):
        self.product_management_button.clicked.connect(self.__presenter.open_product_management)
        self.day_report_button.clicked.connect(self.__presenter.open_day_sale_report_presenter)
        self.month_report_button.clicked.connect(self.__presenter.open_month_sale_report_presenter)
        self.year_report_button.clicked.connect(self.__presenter.open_year_sale_report_presenter)
        self.week_report_button.clicked.connect(self.__presenter.open_week_sale_report_presenter)
        self.custom_report_button.clicked.connect(self.__presenter.open_custom_sale_report_presenter)
        self.year_statistics_button.clicked.connect(self.__presenter.open_year_statistics_presenter)
        self.month_statistics_button.clicked.connect(self.__presenter.open_month_statistics_presenter)
        self.clicked_on_next_frame.connect(self.__show_next_page)
        self.clicked_on_previous_frame.connect(self.__show_previous_page)
        self.clicked_on_about_label.connect(self.__presenter.open_about_presenter)
        self.expenses_button.clicked.connect(self.__presenter.open_expense_management_presenter)

    def __show_next_page(self):
        self.__selected_page_index += 1
        if self.__selected_page_index == len(self.__pages_of_stacked_widget) - 1:
            self.next_frame.hide()
            self.previous_frame.show()
        else:
            self.next_frame.show()
            self.previous_frame.show()
        self.stacked_widget.setCurrentWidget(self.__pages_of_stacked_widget[self.__selected_page_index])
        self.__set_text_on_direction_frame_labels_depending_on_selected_page()

    def __set_text_on_direction_frame_labels_depending_on_selected_page(self):
        selected_page = self.__pages_of_stacked_widget[self.__selected_page_index]
        if selected_page == self.management_widget:
            self.previous_title_label.setText('Estadísticas')
            self.next_title_label.setText('Reportes')
        elif selected_page == self.statistics_widget:
            self.next_title_label.setText('Gestión')
        elif selected_page == self.reports_widget:
            self.previous_title_label.setText('Gestión')

    def __show_previous_page(self):
        self.__selected_page_index -= 1
        if self.__selected_page_index == 0:
            self.next_frame.show()
            self.previous_frame.hide()
        else:
            self.next_frame.show()
            self.previous_frame.show()
        self.stacked_widget.setCurrentWidget(self.__pages_of_stacked_widget[self.__selected_page_index])
        self.__set_text_on_direction_frame_labels_depending_on_selected_page()

    def mouseMoveEvent(self, event: QMouseEvent):
        self.__create_animations()
        self.__start_next_frame_animation_if_mouse_is_hovering()
        self.__start_previous_frame_animation_if_mouse_is_hovering()

    def __create_animations(self):
        if self.__next_frame_animation is None:
            self.__next_frame_animation = GoForwardAndReturnAnimation(
                self.next_frame, b'pos', 30, GoForwardAndReturnAnimation.RIGHT_DIRECTION)
            self.__next_frame_animation.finished.connect(
                self.__start_next_frame_animation_if_mouse_is_hovering
            )

        if self.__previous_frame_animation is None:
            self.__previous_frame_animation = GoForwardAndReturnAnimation(
                self.previous_frame, b'pos', 30, GoForwardAndReturnAnimation.LEFT_DIRECTION
            )
            self.__previous_frame_animation.finished.connect(
                self.__start_previous_frame_animation_if_mouse_is_hovering)

    def __start_next_frame_animation_if_mouse_is_hovering(self):
        if self.next_frame.underMouse() and (
                self.__next_frame_animation.state() == QPropertyAnimation.Stopped):
            self.__next_frame_animation.start()

    def __start_previous_frame_animation_if_mouse_is_hovering(self):
        if self.previous_frame.underMouse() and (
                self.__previous_frame_animation.state() == QPropertyAnimation.Stopped):
            self.__previous_frame_animation.start()

    def mouseReleaseEvent(self, mouse_event: QMouseEvent):
        if self.next_frame.underMouse():
            self.clicked_on_next_frame.emit()
        elif self.previous_frame.underMouse():
            self.clicked_on_previous_frame.emit()
        elif self.about_label.underMouse():
            self.clicked_on_about_label.emit()
