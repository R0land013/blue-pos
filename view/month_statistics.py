from datetime import date, timedelta

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QToolBar, QHBoxLayout
from pyqtgraph import PlotWidget, mkPen, AxisItem, PlotCurveItem, ScatterPlotItem, mkBrush
from qtpy.uic import loadUi

from view.util.text_tool_button import ToolButtonWithTextAndIcon


class MonthStatisticsView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter
        self.__calculated_month_date: date = None

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/month_statistics.ui', self)
        self.__setup_back_tool_button()
        self.__setup_date_edit()
        self.__setup_graph()
        self.__setup_gui_connections()

    def __setup_back_tool_button(self):
        self.tool_bar = QToolBar()
        self.tool_bar_frame.setLayout(QHBoxLayout())
        self.tool_bar_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.tool_bar_frame.layout().setMenuBar(self.tool_bar)

        self.back_button = ToolButtonWithTextAndIcon('Atrás')
        self.back_button.set_icon(QPixmap('./view/ui/images/back.png'))
        self.tool_bar.addWidget(self.back_button)

    def __setup_date_edit(self):
        self.month_date_edit.setMaximumDate(QDate.currentDate())
        self.month_date_edit.setDate(QDate.currentDate())

    def __setup_graph(self):
        layout = self.graph_frame.layout()
        self.plot_widget = PlotWidget(parent=self.graph_frame, background='white', foreground='black')
        layout.addWidget(self.plot_widget)
        self.__set_axis_style()
        self.plot_widget.getPlotItem().getViewBox().setMouseEnabled(x=False, y=False)
        self.plot_widget.getPlotItem().getViewBox().setMenuEnabled(False)
        self.plot_widget.getPlotItem().hideButtons()

    def __set_axis_style(self):
        black_pen = mkPen(color='black')

        bottom_axis: AxisItem = self.plot_widget.getPlotItem().getAxis('bottom')
        bottom_axis.setPen(black_pen)
        bottom_axis.setTextPen(black_pen)

        left_axis: AxisItem = self.plot_widget.getPlotItem().getAxis('left')
        left_axis.setPen(black_pen)
        left_axis.setTextPen(black_pen)

    def __setup_gui_connections(self):
        self.back_button.clicked.connect(self.__presenter.close_presenter)
        self.calculate_button.clicked.connect(self.__set_days_of_month_on_bottom_axis)
        self.calculate_button.clicked.connect(self.__presenter.calculate_economic_day_summaries)

    def __set_days_of_month_on_bottom_axis(self):
        self.__set_calculated_month_date()
        bottom_axis: AxisItem = self.plot_widget.getPlotItem().getAxis('bottom')
        bottom_axis.setTicks(self.__generate_day_of_month_ticks())
        self.plot_widget.getPlotItem().getViewBox().setRange(
            xRange=(1, self.__get_last_day_of_month())
        )

    def __set_calculated_month_date(self):
        qdate: QDate = self.month_date_edit.date()
        self.__calculated_month_date = date(day=1, month=qdate.month(), year=qdate.year())

    def __generate_day_of_month_ticks(self):
        ticks = {}
        current_date = self.__calculated_month_date

        while current_date.month == self.__calculated_month_date.month:
            ticks[current_date.day] = str(current_date.day)

            current_date = current_date + timedelta(days=1)
        return [ticks.items()]

    def __get_last_day_of_month(self) -> int:
        if self.__calculated_month_date.month == 12:
            next_month = 1
        else:
            next_month = self.__calculated_month_date.month + 1

        if next_month == 1:
            first_date_next_month = date(day=1, month=1, year=self.__calculated_month_date.year + 1)
        else:
            first_date_next_month = date(day=1, month=next_month, year=self.__calculated_month_date.year)

        return (first_date_next_month - timedelta(days=1)).day

    def get_selected_month_date(self):
        qdate: QDate = self.month_date_edit.date()
        return date(day=1, month=qdate.month(), year=qdate.year())

    def disable_gui(self, disable: bool):
        self.tool_bar_frame.setDisabled(disable)
        self.main_content_frame.setDisabled(disable)

    def set_status_bar_message(self, message: str):
        self.status_bar_label.setText(message)

    def plot_values(self, x_days_values: list, y_values: list):
        self.plot_widget.getPlotItem().clear()
        self.__set_left_axis_limits(y_range=(0, max(y_values)))
        self.__draw_graph_lines(x_days_values, y_values)
        self.__draw_graph_points(x_days_values, y_values)

    def __set_left_axis_limits(self, y_range: tuple):
        self.plot_widget.getPlotItem().getViewBox().setRange(
            yRange=y_range
        )

    def __draw_graph_lines(self, month_axis: list, y_axis: list):
        plot_curve_item = PlotCurveItem()
        plot_curve_item.setData(month_axis, y_axis,
                                pen=mkPen({'color': '#5599ff', 'width': 2}),
                                antialias=True)
        self.plot_widget.addItem(plot_curve_item)

    def __draw_graph_points(self, month_axis: list, y_axis: list):
        scatter_plot_item = ScatterPlotItem(size=14)
        scatter_plot_item.setData(month_axis, y_axis,
                                  symbol='o',
                                  pen=mkPen({'color': '#5599ff'}),
                                  brush=mkBrush('#5599ff'),
                                  hoverBrush=mkBrush('#59DBFF'),
                                  hoverable=True,
                                  hoverSize=14)
        self.plot_widget.addItem(scatter_plot_item)