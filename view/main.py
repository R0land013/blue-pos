from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QFrame, QApplication
from PyQt5.uic import loadUi


class MainView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__set_up_gui()

    def __set_up_gui(self):
        loadUi('./view/ui/main.ui', self)
        self.wire_up_gui_connections()
        self.__set_window_minimum_size_to_half_of_screen()

    def wire_up_gui_connections(self):
        self.product_management_button.clicked.connect(self.__presenter.open_product_management)
        self.day_report_button.clicked.connect(self.__presenter.open_day_sale_report_presenter)
        self.month_report_button.clicked.connect(self.__presenter.open_month_sale_report_presenter)
        self.year_report_button.clicked.connect(self.__presenter.open_year_sale_report_presenter)

    def __set_window_minimum_size_to_half_of_screen(self):
        q_screen_size = QApplication.primaryScreen().size()
        new_width = q_screen_size.width() // 2
        new_height = q_screen_size.height() // 2
        self.window().setMinimumSize(QSize(new_width, new_height))
