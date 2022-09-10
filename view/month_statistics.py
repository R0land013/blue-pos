from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QToolBar, QHBoxLayout
from qtpy.uic import loadUi

from view.util.text_tool_button import ToolButtonWithTextAndIcon


class MonthStatisticsView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/month_statistics.ui', self)
        self.__setup_back_tool_button()
        self.__setup_gui_connections()

    def __setup_back_tool_button(self):
        self.tool_bar = QToolBar()
        self.tool_bar_frame.setLayout(QHBoxLayout())
        self.tool_bar_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.tool_bar_frame.layout().setMenuBar(self.tool_bar)

        self.back_button = ToolButtonWithTextAndIcon('Atrás')
        self.back_button.set_icon(QPixmap('./view/ui/images/back.png'))
        self.tool_bar.addWidget(self.back_button)

    def __setup_gui_connections(self):
        self.back_button.clicked.connect(self.__presenter.close_presenter)