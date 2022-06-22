from PyQt5.QtCore import pyqtSignal
from easy_mvp.abstract_presenter import AbstractPresenter

from model.entity.models import Product
from model.repository.exc.product import UniqueProductNameException
from model.repository.factory import RepositoryFactory
from model.repository.product import ProductFilter
from model.util.monetary_types import CUPMoney
from presenter.util.thread_worker import PresenterThreadWorker
from view.product import ProductView


class ProductPresenter(AbstractPresenter):

    NEW_PRODUCT_ACTION = 'new_product_action'
    EDIT_PRODUCT_ACTION = 'edit_product_action'

    NEW_PRODUCT_RESULT = 'new_product_result'
    UPDATED_PRODUCT_RESULT = 'updated_product_result'

    PRODUCT = 'product'
    PRODUCT_ID = 'product_id'
    NEW_PRODUCT = 'new_product'
    UPDATED_PRODUCT = 'updated_product'

    def _on_initialize(self):
        self.__initialize_view()
        self.__product_repo = RepositoryFactory.get_product_repository()
        self.__product_to_edit = self.__get_product_if_action_is_to_edit()

    def __get_product_if_action_is_to_edit(self) -> Product:
        if self._get_intent_action() == self.EDIT_PRODUCT_ACTION:
            a_filter = ProductFilter()
            a_filter.id = self._get_intent_data()[self.PRODUCT_ID]
            product = self.__product_repo.get_products_by_filter(a_filter)[0]
            return product
        return None

    def __initialize_view(self):
        view = ProductView(self)
        self._set_view(view)

    def on_view_shown(self):
        self.__hide_labels_depending_on_intent_action()
        self.get_view().set_state_bar_invisible(True)
        self.__fill_product_form_if_action_is_for_editing_product()

    def __hide_labels_depending_on_intent_action(self):
        current_action = self._get_intent_action()
        if current_action == self.NEW_PRODUCT_ACTION:
            self.get_view().set_id_labels_invisible(True)

    def __fill_product_form_if_action_is_for_editing_product(self):
        if self._get_intent_action() == self.EDIT_PRODUCT_ACTION:
            self.__fill_product_form(self.__product_to_edit)

    def __fill_product_form(self, product: Product):
        view = self.get_view()
        view.set_product_id(product.id)
        view.set_name(product.name)
        view.set_description(product.description)
        view.set_price(float(product.price.amount))
        view.set_profit(float(product.profit.amount))
        view.set_quantity(product.quantity)

    def save_product(self):
        if self._get_intent_action() == self.NEW_PRODUCT_ACTION:
            self.__execute_thread_to_insert_new_product()
        elif self._get_intent_action() == self.EDIT_PRODUCT_ACTION:
            self.__execute_thread_to_update_product()

    def __execute_thread_to_insert_new_product(self):
        self.worker = PresenterThreadWorker(self.insert_new_product)
        self.worker.when_started.connect(self.__disable_gui_and_show_operation_message)
        self.worker.error_found.connect(self.__handle_errors_on_product_fields)
        self.worker.finished_without_error.connect(self.__close_presenter_with_new_product_result)
        self.worker.start()

    def insert_new_product(self, error_found: pyqtSignal, finished_without_error: pyqtSignal):
        try:
            product = self.__construct_product_instance_from_view_fields()
            self.__product_repo.insert_product(product)
            self.new_product = product
            finished_without_error.emit()
        except UniqueProductNameException as e:
            error_found.emit(e)

    def __construct_product_instance_from_view_fields(self):
        view = self.get_view()
        name = view.get_name()
        description = view.get_description()
        price = CUPMoney(view.get_price())
        profit = CUPMoney(view.get_profit())
        quantity = view.get_quantity()

        return Product(
            name=name,
            description=description,
            price=price,
            profit=profit,
            quantity=quantity
        )

    def __disable_gui_and_show_operation_message(self):
        self.get_view().set_disabled_view_except_state_bar(True)
        self.get_view().set_state_bar_invisible(False)
        self.get_view().set_state_bar_message('Procesando...')

    def __handle_errors_on_product_fields(self, error: Exception):
        if isinstance(error, UniqueProductNameException):
            self.get_view().set_state_bar_invisible(True)
            self.get_view().show_error_message('Ya existe un producto con el nombre \'{}\'.'.format(error.get_product_name()))
            self.get_view().set_disabled_view_except_state_bar(False)

    def __close_presenter_with_new_product_result(self):
        self._close_this_presenter_with_result({
            self.NEW_PRODUCT: self.new_product
        }, self.NEW_PRODUCT_RESULT)

    def __execute_thread_to_update_product(self):
        self.thread = PresenterThreadWorker(self.__update_product)
        self.thread.when_started.connect(self.__disable_gui_and_show_operation_message)
        self.thread.error_found.connect(self.__handle_errors_on_product_fields)
        self.thread.finished_without_error.connect(self.__close_presenter_with_product_updated_result)
        self.thread.start()

    def __update_product(self, error_found: pyqtSignal, finished_without_error: pyqtSignal):

        try:
            product = self.__construct_product_instance_from_view_fields()
            product.id = self._get_intent_data()[self.PRODUCT_ID]
            self.__product_repo.update_product(product)
            a_filter = ProductFilter()
            a_filter.id = product.id
            self.updated_product = self.__product_repo.get_products_by_filter(a_filter)[0]
            finished_without_error.emit()
        except Exception as e:
            error_found.emit(e)

    def __close_presenter_with_product_updated_result(self):
        self._close_this_presenter_with_result({
            self.UPDATED_PRODUCT: self.updated_product
        }, self.UPDATED_PRODUCT_RESULT)

    def go_back(self):
        self._close_this_presenter()
