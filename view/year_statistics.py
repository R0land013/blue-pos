from datetime import date

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi
from pyqtgraph import PlotWidget, PlotItem, AxisItem


class YearStatisticsView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/year_statistics.ui', self)
        self.__setup_date_edit()
        self.__setup_graph()
        self.__setup_gui_connections()
        self.set_status_bar_message('')

    def __setup_date_edit(self):
        self.year_date_edit.setMaximumDate(QDate.currentDate())
        self.year_date_edit.setDate(QDate.currentDate())

    def __setup_graph(self):
        layout = self.graph_frame.layout()
        self.__plot_widget = PlotWidget(parent=self.graph_frame, background='white')
        layout.addWidget(self.__plot_widget)
        self.__plot_widget.getPlotItem().setTitle('Ganancias Anuales')
        self.__set_month_axis_on_plot_item()
        self.__set_axis_limits()
        self.__plot_widget.getPlotItem().getViewBox().setMouseEnabled(x=False, y=False)
        self.__plot_widget.getPlotItem().getViewBox().setMenuEnabled(False)

    def __set_month_axis_on_plot_item(self):
        months_dict = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
                       7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre',
                       12: 'Diciembre'}
        month_axis = AxisItem(orientation='bottom')
        month_axis.setTicks([months_dict.items()])
        plot_item: PlotItem = self.__plot_widget.getPlotItem()
        plot_item.setAxisItems(axisItems={'bottom': month_axis})

    def __set_axis_limits(self, min_y: int = 0, max_y: int = 1000):
        self.__plot_widget.getPlotItem().getViewBox().setRange(
            xRange=(1, 12),  # Enero y Diciembre
            yRange=(min_y, max_y)
        )

    def __setup_gui_connections(self):
        self.back_button.clicked.connect(self.__presenter.close_presenter)
        self.calculate_button.clicked.connect(self.__presenter.calculate_economic_month_summaries)

    def get_selected_year(self) -> int:
        return self.year_date_edit.date().year()

    def disable_gui(self, disable: bool):
        self.main_content_frame.setDisabled(disable)
        self.tool_bar_frame.setDisabled(disable)

    def set_status_bar_message(self, message: str):
        self.status_bar_label.setText(message)

    def plot_values(self, month_axis: list, y_axis: list):
        plot_item: PlotItem = self.__plot_widget.getPlotItem()
        plot_item.clear()
        self.__set_axis_limits(min(y_axis), max(y_axis))
        plot_item.plot(month_axis, y_axis, symbol='o')

