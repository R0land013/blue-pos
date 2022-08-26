from easy_mvp.abstract_presenter import AbstractPresenter

from model.entity.models import Sale
from model.repository.factory import RepositoryFactory
from model.util.monetary_types import CUPMoney
from presenter.util.thread_worker import PresenterThreadWorker
from view.edit_sale import EditSaleView


class EditSalePresenter(AbstractPresenter):

    SALE = 'sale'
    UPDATED_SALE = 'updated_sale'

    UPDATED_SALE_RESULT = 'updated_sale_result'

    def _on_initialize(self):
        self.__initialize_view()
        self.__sale = self._get_intent_data()[self.SALE]
        self.__sale_repo = RepositoryFactory.get_sale_repository()

    def __initialize_view(self):
        view = EditSaleView(self)
        self._set_view(view)

    def get_default_window_title(self) -> str:
        return 'Editar venta'

    def on_view_shown(self):
        self.get_view().hide_status_bar(True)
        self.__fill_form_fields()

    def __fill_form_fields(self):
        view = self.get_view()
        view.set_product_name(self.__sale.product.name)
        view.set_sale_id(self.__sale.id)
        view.set_paid_money(float(self.__sale.price.amount))
        view.set_cost_money(float(self.__sale.cost.amount))
        view.set_sale_date(self.__sale.date)

    def close_presenter(self):
        self._close_this_presenter()

    def update_sale_and_close_presenter(self):
        if self.get_view().ask_user_to_confirm_no_profit_sale_if_needed():

            self.__updated_sale = self.__construct_updated_sale()
            self.thread = PresenterThreadWorker(self.__update_sale)
            self.thread.when_started.connect(self.__disable_controls_and_show_processing_message)
            self.thread.finished_without_error.connect(
                self.__close_this_and_notify_below_presenter)
            self.thread.start()

    def __update_sale(self, thread: PresenterThreadWorker = None):
        self.__sale_repo.update_sale(self.__updated_sale)
        thread.finished_without_error.emit()

    def __construct_updated_sale(self) -> Sale:
        return Sale(
            id=self.__sale.id,
            product_id=self.__sale.product_id,
            price=CUPMoney(self.get_view().get_paid_money_as_str()),
            cost=CUPMoney(self.get_view().get_cost_money_as_str()),
            date=self.get_view().get_sale_date()
        )

    def __close_this_and_notify_below_presenter(self):
        result_data = {self.UPDATED_SALE: self.__updated_sale}
        self._close_this_presenter_with_result(result_data, self.UPDATED_SALE_RESULT)

    def __disable_controls_and_show_processing_message(self):
        self.get_view().hide_status_bar(False)
        self.get_view().set_status_bar_message('Procesando..')
