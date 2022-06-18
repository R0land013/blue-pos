from easy_mvp.abstract_presenter import AbstractPresenter

from model.entity.models import Product
from model.repository.factory import RepositoryFactory
from model.repository.product import ProductFilter
from model.util.monetary_types import CUPMoney
from view.product import ProductView


class ProductPresenter(AbstractPresenter):

    NEW_PRODUCT_ACTION = 'new_product_action'
    EDIT_PRODUCT_ACTION = 'edit_product_action'

    PRODUCT = 'product'
    PRODUCT_ID = 'product_id'

    def _on_initialize(self):
        self.__initialize_view()
        self.__product_repo = RepositoryFactory.get_product_repository()

    def __initialize_view(self):
        view = ProductView(self)
        self._set_view(view)

    def on_view_shown(self):
        self.__hide_labels_depending_on_intent_action()
        self.__fill_product_form_if_action_is_for_editing_product()

    def __hide_labels_depending_on_intent_action(self):
        current_action = self._get_intent_action()
        if current_action == self.NEW_PRODUCT_ACTION:
            self.get_view().set_id_labels_invisible(True)

    def __fill_product_form_if_action_is_for_editing_product(self):
        if self._get_intent_action() == self.EDIT_PRODUCT_ACTION:
            a_filter = ProductFilter()
            a_filter.id = self._get_intent_data()[self.PRODUCT_ID]
            product = self.__product_repo.get_products_by_filter(a_filter)[0]
            self.__fill_product_form(product)

    def __fill_product_form(self, product: Product):
        view = self.get_view()
        view.set_product_id(product.id)
        view.set_name(product.name)
        view.set_description(product.description)
        view.set_price(float(product.price.amount))
        view.set_profit(float(product.profit.amount))
        view.set_quantity(product.quantity)

    def save_product(self):
        view = self.get_view()
        name = view.get_name()
        description = view.get_description()
        price = CUPMoney(view.get_price())
        profit = CUPMoney(view.get_profit())
        quantity = view.get_quantity()

        product = Product(
            name=name,
            description=description,
            price=price,
            profit=profit,
            quantity=quantity
        )

        self.__product_repo.insert_product(product)
        self._close_this_presenter()

    def go_back(self):
        self._close_this_presenter()
