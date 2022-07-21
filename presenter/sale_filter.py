from easy_mvp.abstract_presenter import AbstractPresenter

from model.repository.sale import SaleFilter
from view.sale_filter import SaleFilterView


class SaleFilterPresenter(AbstractPresenter):

    NEW_FILTER_DATA = 'new_filter_data'
    FILTER_BY_PRODUCT_ID_LIST_DATA = 'product_id_list_data'

    NEW_FILTER_RESULT = 'new_filter_result'

    def _on_initialize(self):
        self.__initialize_view()

    def __initialize_view(self):
        self._set_view(SaleFilterView(self))

    def close_presenter(self):
        self._close_this_presenter()

    def create_sale_filter_and_close(self):
        sale_filter = SaleFilter()
        initial_date = self.get_view().get_initial_date()
        final_date = self.get_view().get_final_date()

        sale_filter.minimum_date = initial_date
        sale_filter.maximum_date = final_date
        if self.FILTER_BY_PRODUCT_ID_LIST_DATA in self._get_intent_data():
            sale_filter.product_id_list = self._get_intent_data()[self.FILTER_BY_PRODUCT_ID_LIST_DATA]

        result_data = {self.NEW_FILTER_DATA: sale_filter}
        self._close_this_presenter_with_result(result_data, self.NEW_FILTER_RESULT)
