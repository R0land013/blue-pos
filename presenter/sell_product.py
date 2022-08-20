from datetime import date

from easy_mvp.abstract_presenter import AbstractPresenter

from model.entity.models import Sale
from model.repository.factory import RepositoryFactory
from presenter.util.thread_worker import PresenterThreadWorker
from view.sell_product import MakeSaleView


class MakeSalePresenter(AbstractPresenter):

    NEW_SALES_RESULT = 'new_sales_result'

    PRODUCT = 'product'
    NEW_SALES = 'new_sales'

    def _on_initialize(self):
        self.__initialize_view()
        self.__product = self._get_intent_data()[self.PRODUCT]
        self.__sale_repo = RepositoryFactory.get_sale_repository()

    def __initialize_view(self):
        view = MakeSaleView(self)
        self._set_view(view)

    def on_view_shown(self):
        self.get_view().set_limit_of_sales(self.__product.quantity)
        self.set_sale_result_by_quantity()
        self.get_view().hide_status_bar(True)

    def set_sale_result_by_quantity(self):
        sale_quantity = self.get_view().get_sale_quantity()
        money_to_pay = self.__product.price * sale_quantity
        self.get_view().set_money_to_pay(str(money_to_pay.amount))

    def make_sales_and_close_presenter(self):
        self.__sale_quantity = self.get_view().get_sale_quantity()
        self.__mock_sale = self.__create_mock_sale_from_product()
        self.thread = PresenterThreadWorker(self.__do_sales)
        self.thread.when_started.connect(self.__show_message_and_disable_controls)
        self.thread.finished_without_error.connect(
            self.__close_this_and_notify_changes_to_below_presenter)
        self.thread.start()

    def __do_sales(self, thread: PresenterThreadWorker):
        self.__new_sales = self.__sale_repo.insert_sales(self.__mock_sale, self.__sale_quantity)
        thread.finished_without_error.emit()

    def __show_message_and_disable_controls(self):
        self.get_view().hide_status_bar(False)
        self.get_view().set_status_bar_message('Procesando...')
        self.get_view().disable_all_view_except_status_bar(True)

    def __close_this_and_notify_changes_to_below_presenter(self):
        result_data = {self.NEW_SALES: self.__new_sales}
        self._close_this_presenter_with_result(result_data, self.NEW_SALES_RESULT)

    def __create_mock_sale_from_product(self):
        return Sale(
            product_id=self.__product.id,
            price=self.__product.price,
            cost=self.__product.cost,
            date=self.get_view().get_sale_date()
        )

    def cancel_sale(self):
        self._close_this_presenter()
