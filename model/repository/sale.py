from datetime import date

from sqlalchemy import insert, update, select, delete, cast, Numeric, type_coerce, asc, desc

from model.entity.models import Product, Sale
from sqlalchemy.orm import Session

from model.repository.exc.product import NonExistentProductException, NoPositivePriceException, NegativeProfitException, \
    TooMuchProfitException
from model.repository.exc.sale import NoEnoughProductQuantityException, NonExistentSaleException, \
    ChangeProductIdInSaleException
from model.repository.observer import RepositoryObserver
from model.util.monetary_types import CUPMoney


class SaleFilter:

    ID = 'id'
    PRODUCT_ID = 'product_id'
    SALE_DATE = 'sale_date'
    PRICE = 'price'
    PROFIT = 'profit'

    def __init__(self):
        self.__product_id_list = None
        self.__minimum_date = None
        self.__maximum_date = None
        self.__sale_id_list = None
        self.__sorted_by = None
        self.__ascending_order = True

    @property
    def sale_id_list(self):
        return self.__sale_id_list

    @sale_id_list.setter
    def sale_id_list(self, value: list):
        self.__sale_id_list = value

    @property
    def product_id_list(self) -> list:
        return self.__product_id_list

    @product_id_list.setter
    def product_id_list(self, value: list):
        self.__product_id_list = value

    @property
    def minimum_date(self) -> date:
        return self.__minimum_date

    @minimum_date.setter
    def minimum_date(self, value: date):
        self.__minimum_date = value

    @property
    def maximum_date(self) -> date:
        return self.__maximum_date

    @maximum_date.setter
    def maximum_date(self, value: date):
        self.__maximum_date = value

    @property
    def sorted_by(self) -> str:
        return self.__sorted_by

    @sorted_by.setter
    def sorted_by(self, value: str):
        self.__sorted_by = value

    @property
    def ascending_order(self) -> bool:
        return self.__ascending_order

    @ascending_order.setter
    def ascending_order(self, value: bool):
        self.__ascending_order = value


class SaleRepository(RepositoryObserver):

    def __init__(self, session: Session):
        super().__init__()
        self.__session = session

    def insert_sales(self, sale: Sale, quantity: int) -> list:
        self.__check_quantity_is_positive(quantity)
        self.__check_price_is_positive(sale)
        self.__check_profit_is_not_negative(sale)
        self.__check_profit_is_no_higher_than_price(sale)
        self.__check_product_exists(sale)
        self.__check_there_are_enough_products(sale, quantity)

        sales = self.__execute_insertion_and_return_sales(sale, quantity)
        self.__execute_product_quantity_update(sale, quantity)
        self.__session.commit()
        self._notify_on_data_changed_listeners()
        return sales

    def __check_quantity_is_positive(self, quantity: int):
        if quantity <= 0:
            raise ValueError('The quantity of sales must be positive.')

    def __check_price_is_positive(self, sale: Sale):
        if not sale.price > CUPMoney('0.00'):
            raise NoPositivePriceException()

    def __check_profit_is_not_negative(self, sale: Sale):
        if sale.profit < CUPMoney('0.00'):
            raise NegativeProfitException()

    def __check_profit_is_no_higher_than_price(self, sale: Sale):
        if sale.profit > sale.price:
            raise TooMuchProfitException(sale.price, sale.profit)

    def __get_product_by_id(self, product_id: int) -> Product:
        return self.__session.scalar(select(Product).where(Product.id == product_id))

    def __check_product_exists(self, sale: Sale):
        read_product = self.__get_product_by_id(sale.product_id)
        if read_product is None:
            nonexistent_product = Product()
            nonexistent_product.id = sale.product_id
            raise NonExistentProductException(nonexistent_product)

    def __check_there_are_enough_products(self, sale: Sale, quantity_of_sales):
        read_product = self.__get_product_by_id(sale.product_id)
        if read_product.quantity - quantity_of_sales < 0:
            raise NoEnoughProductQuantityException(read_product.quantity)

    def __execute_insertion_and_return_sales(self, sale: Sale, quantity: int) -> list:
        sales = []
        for i in range(quantity):
            a_sale = Sale(
                product_id=sale.product_id,
                date=sale.date,
                price=sale.price,
                profit=sale.profit
            )
            sales.append(a_sale)
        self.__session.add_all(sales)
        return sales

    def __execute_product_quantity_update(self, sale: Sale, sale_quantity: int):
        product = self.__session.scalar(select(Product).where(Product.id == sale.product_id))

        self.__session.execute(
            update(Product)
            .where(Product.id == sale.product_id)
            .values(quantity=product.quantity - sale_quantity)
        )

    def delete_sale(self, sale_to_delete: Sale):
        self.__check_sale_exists(sale_to_delete)
        self.__check_product_exists(sale_to_delete)
        self.__increase_product_quantity(sale_to_delete)

        self.__session.execute(
            delete(Sale)
            .where(Sale.id == sale_to_delete.id)
        )
        self.__session.commit()
        self._notify_on_data_changed_listeners()

    def delete_sales(self, sale_id_list: list):
        self.__check_sales_exists(sale_id_list)
        self.__increase_quantity_of_associated_products(sale_id_list)

        self.__execute_sale_deletion(sale_id_list)
        self.__session.commit()

    def __check_sales_exists(self, sale_id_list: list):
        for sale_id in sale_id_list:
            sale = self.__get_sale_by_id(sale_id)
            if sale is None:
                raise NonExistentSaleException(Sale(id=sale_id))

    def __increase_quantity_of_associated_products(self, sale_id_list: list):
        for sale_id in sale_id_list:
            sale = self.__get_sale_by_id(sale_id)
            product = sale.product
            self.__session.execute(update(Product)
                                   .where(Product.id == product.id)
                                   .values(quantity=product.quantity + 1))

    def __execute_sale_deletion(self, sale_id_list: list):
        self.__session.execute(delete(Sale)
                               .where(Sale.id.in_(sale_id_list)))

    def __get_sale_by_id(self, sale_id: int):
        return self.__session.scalar(select(Sale).where(Sale.id == sale_id))

    def __check_sale_exists(self, sale_to_delete):
        read_sale = self.__get_sale_by_id(sale_to_delete.id)
        if read_sale is None:
            raise NonExistentSaleException(sale_to_delete)

    def __increase_product_quantity(self, sale: Sale):
        product = self.__get_product_by_id(sale.product_id)

        self.__session.execute(
            update(Product)
            .where(Product.id == sale.product_id)
            .values(quantity=product.quantity + 1)
        )

    def update_sale(self, sale: Sale):
        self.__check_price_is_positive(sale)
        self.__check_profit_is_not_negative(sale)
        self.__check_profit_is_no_higher_than_price(sale)
        self.__check_sale_exists(sale)
        self.__check_product_id_is_not_changed_in_sale(sale)

        self.__execute_update_operation(sale)
        self.__session.commit()
        self._notify_on_data_changed_listeners()

    def __check_sale_exists(self, sale: Sale):
        read_sale = self.__session.scalar(select(Sale).where(Sale.id == sale.id))
        if read_sale is None:
            raise NonExistentSaleException(sale)

    def __check_product_id_is_not_changed_in_sale(self, sale: Sale):
        read_sale = self.__get_sale_by_id(sale.id)
        if read_sale.product_id != sale.product_id:
            raise ChangeProductIdInSaleException()

    def __execute_update_operation(self, sale: Sale):
        self.__session.execute(
            update(Sale)
                .where(Sale.id == sale.id)
                .values(
                date=sale.date,
                price=sale.price,
                profit=sale.profit
            )
        )

    def get_all_sales(self) -> list:
        return self.__session.scalars(select(Sale)).all()

    def get_sales_by_filter(self, the_filter: SaleFilter) -> list:
        filter_query = SaleRepository.__create_filter_query(the_filter)
        return self.__session.scalars(filter_query).all()

    @staticmethod
    def __create_filter_query(the_filter: SaleFilter):
        query = select(Sale)

        if the_filter.minimum_date is not None:
            query = query.where(Sale.date >= the_filter.minimum_date)
        if the_filter.maximum_date is not None:
            query = query.where(Sale.date <= the_filter.maximum_date)

        if the_filter.product_id_list is not None:
            query = query.where(Sale.product_id.in_(the_filter.product_id_list))

        if the_filter.sale_id_list is not None:
            query = query.where(Sale.id.in_(the_filter.sale_id_list))

        query = SaleRepository.__add_order_by_clause(query, the_filter)

        return query

    @staticmethod
    def __add_order_by_clause(query, the_filter: SaleFilter):
        if the_filter.sorted_by is None:
            return query

        column = None
        is_money_column = False

        if the_filter.sorted_by == SaleFilter.ID:
            column = Sale.id
        elif the_filter.sorted_by == SaleFilter.PRODUCT_ID:
            column = Sale.product_id
        elif the_filter.sorted_by == SaleFilter.SALE_DATE:
            column = Sale.date
        elif the_filter.sorted_by == SaleFilter.PRODUCT_ID:
            column = Sale.product_id
        elif the_filter.sorted_by == SaleFilter.PRICE:
            column = Sale.price
            is_money_column = True
        elif the_filter.sorted_by == SaleFilter.PROFIT:
            column = Sale.profit
            is_money_column = True

        if is_money_column:
            if the_filter.ascending_order:
                return query.order_by(asc(cast(column, Numeric)))
            return query.order_by(desc(cast(column, Numeric)))

        if the_filter.ascending_order:
            column = column.asc()
        else:
            column = column.desc()

        return query.order_by(column)
