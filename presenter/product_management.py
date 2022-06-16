from easy_mvp.abstract_presenter import AbstractPresenter

from model.repository.factory import RepositoryFactory
from view.product_management import ProductManagementView


class ProductManagementPresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__initialize_view()

    def __initialize_view(self):
        view = ProductManagementView(self)
        self._set_view(view)

    def return_to_main(self):
        self._close_this_presenter()

    def on_view_shown(self):
        self.__fill_table()

    def __fill_table(self):
        view = self.get_view()
        product_repo = RepositoryFactory.get_product_repository()
        products = product_repo.get_all_products()
        print(products)
        for index in range(len(products)):
            row = index
            a_product = products[index]
            view.add_empty_row_at_the_end_of_table()

            view.set_cell_in_table(row, ProductManagementView.ID_COLUMN, a_product.id)
            view.set_cell_in_table(row, ProductManagementView.NAME_COLUMN, a_product.name)
            view.set_cell_in_table(row, ProductManagementView.DESCRIPTION_COLUMN, a_product.description)
            view.set_cell_in_table(row, ProductManagementView.PRICE_COLUMN, a_product.price)
            view.set_cell_in_table(row, ProductManagementView.PROFIT_COLUMN, a_product.profit)
            view.set_cell_in_table(row, ProductManagementView.QUANTITY_COLUMN, a_product.quantity)
        view.resize_table_columns_to_contents()
