from easy_mvp.abstract_presenter import AbstractPresenter

from model.repository.expense import ExpenseFilter
from view.expense_filter import ExpenseFilterView


class ExpenseFilterPresenter(AbstractPresenter):

    EXPENSE_FILTER_DATA = 'expense_filter_data'
    CREATED_EXPENSE_FILTER_DATA = 'new_expense_filter_data'

    CREATED_EXPENSE_FILTER_RESULT = 'created_expense_filter_result'

    def get_default_window_title(self) -> str:
        return 'Filtrar gastos'

    def _on_initialize(self):
        self._set_view(ExpenseFilterView(self))
        self.__expense_filter: ExpenseFilter = None

        if self._get_intent_data()[self.EXPENSE_FILTER_DATA] is not None:
            self.__expense_filter = self._get_intent_data()[self.EXPENSE_FILTER_DATA]
            self.__fill_fields_by_expense_filter()

    def __fill_fields_by_expense_filter(self):
        if self.__expense_filter.phrase is not None:
            self.get_view().set_phrase_check_box_checked(True)
            self.get_view().set_phrase(self.__expense_filter.phrase)

        if self.__expense_filter.minimum_date is not None:
            self.get_view().set_initial_date_check_box_checked(True)
            self.get_view().set_initial_date(self.__expense_filter.minimum_date)

        if self.__expense_filter.maximum_date is not None:
            self.get_view().set_final_date_check_box_checked(True)
            self.get_view().set_final_date(self.__expense_filter.maximum_date)

    def close_presenter(self):
        self._close_this_presenter()

    def return_filter_to_caller_of_this_presenter(self):
        the_filter = self.__construct_filter_from_fields()
        result_data = {self.CREATED_EXPENSE_FILTER_DATA: the_filter}
        self._close_this_presenter_with_result(result_data, self.CREATED_EXPENSE_FILTER_RESULT)

    def __construct_filter_from_fields(self):
        the_filter = ExpenseFilter()
        the_filter.phrase = self.get_view().get_phrase()
        the_filter.minimum_date = self.get_view().get_initial_date()
        the_filter.maximum_date = self.get_view().get_final_date()
        return the_filter
