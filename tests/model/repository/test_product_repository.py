import unittest
from model.repository.exc.product import UniqueProductNameException, NonExistentProductException, \
    InvalidProductQuantityException, NoPositivePriceException, NegativeProfitException, TooMuchProfitException
from model.repository.factory import RepositoryFactory
from model.repository.product import ProductFilter
from model.util.monetary_types import CUPMoney
from tests.util.generators.product import ProductGenerator
from tests.util.general import TEST_DB_URL, get_all_products_in_database, insert_product_and_return_it, \
    get_one_product_from_database, insert_products_in_database_and_return_them, delete_all_products_from_database, \
    insert_sales_and_return_them, get_all_sales_from_database
from tests.util.generators.sale import SaleGenerator


class TestProductRepository(unittest.TestCase):

    def setUp(self):
        self.product_repository = RepositoryFactory.get_product_repository(TEST_DB_URL)

    def tearDown(self):
        RepositoryFactory.close_session()
        delete_all_products_from_database()

    def test_products_are_inserted_successfully(self):
        products = ProductGenerator.generate_products_by_quantity(3)

        for a_product in products:
            self.product_repository.insert_product(a_product)
        inserted_products = get_all_products_in_database()

        self.assertEqual(inserted_products, products)

    def test_product_inserted_with_used_name_raise_exception(self):
        product = ProductGenerator.generate_one_product()

        self.product_repository.insert_product(product)

        self.assertRaises(UniqueProductNameException, self.product_repository.insert_product, product)

    def test_product_inserted_with_used_name_in_uppercase_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        self.product_repository.insert_product(product)

        product.name = product.name.upper()

        self.assertRaises(UniqueProductNameException, self.product_repository.insert_product,
                          product)

    def test_product_inserted_with_negative_quantity_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product.quantity = -1
        self.assertRaises(InvalidProductQuantityException, self.product_repository.insert_product,
                          product)

    def test_product_inserted_with_negative_price_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product.price = CUPMoney('-1.00')

        self.assertRaises(NoPositivePriceException, self.product_repository.insert_product,
                          product)

    def test_product_inserted_with_zero_price_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product.price = CUPMoney('0.00')

        self.assertRaises(NoPositivePriceException, self.product_repository.insert_product,
                          product)

    def test_product_inserted_with_negative_profit_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product.profit = CUPMoney('-1.00')

        self.assertRaises(NegativeProfitException, self.product_repository.insert_product,
                          product)

    def test_insert_product_with_higher_profit_than_price_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product.price = CUPMoney('10.00')
        product.profit = CUPMoney('11.00')

        self.assertRaises(TooMuchProfitException, self.product_repository.insert_product,
                          product)

    def test_product_is_deleted_successfully(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)

        self.product_repository.delete_product(product)

        products = get_all_products_in_database()
        self.assertEqual(len(products), 0)

    def test_trying_to_delete_nonexistent_product_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product.id = 1

        self.assertRaises(NonExistentProductException, self.product_repository.delete_product,
                          product)

    def test_delete_products(self):
        products = ProductGenerator.generate_products_by_quantity(3)
        p1, p2, p3 = products
        insert_products_in_database_and_return_them(products)

        self.product_repository.delete_products([p1.id, p3.id])

        remaining_products = get_all_products_in_database()
        self.assertEqual(remaining_products, [p2])

    def test_try_to_delete_nonexistent_products_raises_exception(self):
        products = ProductGenerator.generate_products_by_quantity(2)
        p1, p2 = products
        p1.id, p2.id = 1, 2

        self.assertRaises(NonExistentProductException, self.product_repository.delete_products,
                          [p1.id, p2.id])

    def test_deleting_products_also_deletes_associated_sales(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sales = SaleGenerator.generate_sales_from_product(product, 5)
        sales = insert_sales_and_return_them(sales)

        self.product_repository.delete_products([product.id])

        self.assertEqual(get_all_sales_from_database(), [])

    def test_product_is_updated_successfully(self):
        old_product = ProductGenerator.generate_one_product()

        old_product = insert_product_and_return_it(old_product)
        new_product = ProductGenerator.generate_one_product()
        new_product.id = old_product.id
        new_product.price = CUPMoney('55.00')
        new_product.profit = CUPMoney('45.00')
        new_product.quantity = 13

        self.product_repository.update_product(new_product)

        updated_product = get_one_product_from_database()
        self.assertTrue(old_product != updated_product and new_product == updated_product)

    def test_trying_to_update_nonexistent_product_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product.id = 1

        new_product = ProductGenerator.generate_one_product()
        new_product.id = product.id

        self.assertRaises(NonExistentProductException, self.product_repository.update_product,
                          new_product)

    def test_trying_to_update_product_using_existent_name_raises_exception(self):
        first_product, second_product = ProductGenerator.generate_products_by_quantity(2)
        first_product = insert_product_and_return_it(first_product)
        second_product = insert_product_and_return_it(second_product)

        new_product = ProductGenerator.generate_one_product()
        new_product.id = first_product.id
        new_product.name = second_product.name

        self.assertRaises(UniqueProductNameException, self.product_repository.update_product,
                          new_product)

    def test_trying_to_update_product_using_same_name_does_not_raise_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        new_product = ProductGenerator.generate_one_product()
        new_product.id = product.id
        new_product.name = product.name

        self.product_repository.update_product(new_product)

        updated_product = get_one_product_from_database()
        self.assertEqual(updated_product, new_product)

    def test_product_updated_with_negative_quantity_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        product.quantity = -1

        self.assertRaises(InvalidProductQuantityException, self.product_repository.update_product,
                          product)

    def test_product_updated_with_negative_price_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        product.price = CUPMoney('-1.00')

        self.assertRaises(NoPositivePriceException, self.product_repository.update_product,
                          product)

    def test_product_updated_with_zero_price_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        product.price = CUPMoney('0.00')

        self.assertRaises(NoPositivePriceException, self.product_repository.update_product,
                          product)

    def test_product_updated_with_negative_profit_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        product.profit = CUPMoney('-1.00')

        self.assertRaises(NegativeProfitException, self.product_repository.update_product,
                          product)

    def test_update_product_with_profit_higher_than_price_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        product.price = CUPMoney('10.00')
        product.profit = CUPMoney('11.00')

        self.assertRaises(TooMuchProfitException, self.product_repository.update_product,
                          product)

    def test_get_all_products_returns_empty_list(self):
        empty_list = []

        retrieved_list = self.product_repository.get_all_products()

        self.assertEqual(retrieved_list, empty_list)

    def test_get_all_products_returns_nonempty_list(self):
        products = ProductGenerator.generate_products_by_quantity(3)
        insert_products_in_database_and_return_them(products)
        products = get_all_products_in_database()

        retrieved_products = self.product_repository.get_all_products()
        self.assertEqual(products, retrieved_products)

    def test_get_products_by_filter_id(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        the_filter = ProductFilter()
        the_filter.id = product.id

        filtered_products = self.product_repository.get_products_by_filter(the_filter)

        self.assertEqual([product], filtered_products)

    def test_get_products_by_filter_using_name(self):
        products = ProductGenerator.generate_products_by_quantity(2)
        product_1, product_2 = products
        product_1.name = 'Running shoes'
        product_2.name = 'Smart watch'
        products = insert_products_in_database_and_return_them(products)
        product_1, product_2 = products

        the_filter = ProductFilter()
        the_filter.name = 'TC'
        filtered_products = self.product_repository.get_products_by_filter(the_filter)

        self.assertEqual([product_2], filtered_products)

    def test_get_products_by_filter_using_description(self):
        products = ProductGenerator.generate_products_by_quantity(3)
        product_0, product_1, product_2 = products
        product_0.description = 'A pretty picture'
        product_1.description = 'A small shoe'
        product_2.description = 'Cellphone protection'
        products = insert_products_in_database_and_return_them(products)

        the_filter = ProductFilter()
        the_filter.description = 'LL'
        filtered_products = self.product_repository.get_products_by_filter(the_filter)

        self.assertEqual([product_1, product_2], filtered_products)

    def test_get_products_by_filter_using_price_range(self):
        products = ProductGenerator.generate_products_by_quantity(4)
        product_0, product_1, product_2, product_3 = products
        product_0.price = CUPMoney('13')
        product_1.price = CUPMoney('17')
        product_2.price = CUPMoney('18')
        product_3.price = CUPMoney('23')
        products = insert_products_in_database_and_return_them(products)

        the_filter = ProductFilter()
        the_filter.more_than_price = CUPMoney('13')
        the_filter.less_than_price = CUPMoney('18')
        filtered_products = self.product_repository.get_products_by_filter(the_filter)

        self.assertEqual([product_0, product_1, product_2], filtered_products)

    def test_get_products_by_filter_using_profit_range(self):
        products = ProductGenerator.generate_products_by_quantity(4)
        product_0, product_1, product_2, product_3 = products
        product_0.profit = CUPMoney('13')
        product_1.profit = CUPMoney('17')
        product_2.profit = CUPMoney('18')
        product_3.profit = CUPMoney('23')
        products = insert_products_in_database_and_return_them(products)

        the_filter = ProductFilter()
        the_filter.more_than_profit = CUPMoney('13')
        the_filter.less_than_profit = CUPMoney('18')
        filtered_products = self.product_repository.get_products_by_filter(the_filter)

        self.assertEqual([product_0, product_1, product_2], filtered_products)

    def test_get_products_by_filter_using_quantity_range(self):
        products = ProductGenerator.generate_products_by_quantity(4)
        product_0, product_1, product_2, product_3 = products
        product_0.quantity = 13
        product_1.quantity = 17
        product_2.quantity = 18
        product_3.quantity = 23
        products = insert_products_in_database_and_return_them(products)

        the_filter = ProductFilter()
        the_filter.more_than_quantity = 13
        the_filter.less_than_quantity = 18
        filtered_products = self.product_repository.get_products_by_filter(the_filter)

        self.assertEqual([product_0, product_1, product_2], filtered_products)
