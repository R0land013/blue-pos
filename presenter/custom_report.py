from easy_mvp.abstract_presenter import AbstractPresenter

from model.repository.sale import SaleFilter
from view.custom_report import CustomSaleReportView


class CustomSaleReportPresenter(AbstractPresenter):

    def _on_initialize(self):
        self._set_view(CustomSaleReportView(self))

    def close_presenter(self):
        self._close_this_presenter()

    def open_custom_report_visualizer_presenter(self):
        sale_filter = self.__create_sale_filter()
        print("""
        name: '{}',
        description: '{}',
        minimum_date: {},
        maximum_date: {},
        sorted_by: {},
        ascending_order: {}
        """.format(
            self.get_view().get_report_name(),
            self.get_view().get_report_description(),
            sale_filter.minimum_date,
            sale_filter.maximum_date,
            sale_filter.sorted_by,
            sale_filter.ascending_order
        ))

    def __create_sale_filter(self) -> SaleFilter:
        sale_filter = SaleFilter()
        sale_filter.minimum_date = self.get_view().get_initial_date()
        sale_filter.maximum_date = self.get_view().get_final_date()
        sale_filter.sorted_by = self.__get_column_to_order_sale_report()
        sale_filter.ascending_order = self.get_view().is_ascending_order()
        return sale_filter

    def __get_column_to_order_sale_report(self):
        column = self.get_view().get_order_by_report_column()
        if column == CustomSaleReportView.SALE_ID_REPORT_COLUMN:
            return SaleFilter.ID
        elif column == CustomSaleReportView.PAID_REPORT_COLUMN:
            return SaleFilter.PRICE
        elif column == CustomSaleReportView.PROFIT_REPORT_COLUMN:
            return SaleFilter.PROFIT
        return SaleFilter.SALE_DATE
