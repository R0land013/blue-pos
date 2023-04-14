from easy_mvp.abstract_presenter import AbstractPresenter

from model.repository.sale import SaleFilter
from view.sale_filter import SaleFilterView


class SaleFilterPresenter(AbstractPresenter):

    NEW_FILTER_DATA = 'new_filter_data'
    FILTER_BY_PRODUCT_ID_LIST_DATA = 'product_id_list_data'
    APPLIED_FILTER = 'filter_to_fill_form'

    NEW_FILTER_RESULT = 'new_filter_result'

    def _on_initialize(self):
        self.__initialize_view()
        self.__applied_filter: SaleFilter = self._get_intent_data()[self.APPLIED_FILTER]

    def __initialize_view(self):
        self._set_view(SaleFilterView(self))

    def on_view_shown(self):
        self.__fill_form_if_there_is_an_applied_filter()

    def __fill_form_if_there_is_an_applied_filter(self):
        if self.__applied_filter is None: return

        view = self.get_view()
        
        if self.__applied_filter.minimum_date is not None:
            view.set_initial_date_check_box_checked(True) 
            view.set_initial_date(self.__applied_filter.minimum_date)
        
        if self.__applied_filter.maximum_date is not None:
            view.set_final_date_check_box_checked(True)
            view.set_final_date(self.__applied_filter.maximum_date)

    def close_presenter(self):
        self._close_this_presenter()

    def get_default_window_title(self) -> str:
        return 'Filtrar ventas'

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
