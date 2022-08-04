from easy_mvp.abstract_presenter import AbstractPresenter

from view.custom_report_visualization import CustomReportVisualizationView


class CustomReportVisualizationPresenter(AbstractPresenter):

    def _on_initialize(self):
        self._set_view(CustomReportVisualizationView(self))

    def close_presenter(self):
        self._close_this_presenter()
