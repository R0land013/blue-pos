from easy_mvp.abstract_presenter import AbstractPresenter
from view.edit_sale import EditSaleView


class EditSalePresenter(AbstractPresenter):

    SALE = 'sale'

    def _on_initialize(self):
        self.__initialize_view()
        self.__sale = self._get_intent_data()[self.SALE]

    def __initialize_view(self):
        view = EditSaleView(self)
        self._set_view(view)

    def on_view_shown(self):
        self.get_view().hide_status_bar(True)
        self.__fill_form_fields()

    def __fill_form_fields(self):
        view = self.get_view()
        view.set_product_name(self.__sale.product.name)
        view.set_sale_id(self.__sale.id)
        view.set_paid_money(float(self.__sale.price.amount))
        view.set_profit_money(float(self.__sale.profit.amount))
        view.set_sale_date(self.__sale.date)

    def close_presenter(self):
        self._close_this_presenter()