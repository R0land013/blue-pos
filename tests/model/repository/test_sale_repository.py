import unittest
from datetime import date, timedelta
from model.repository.exc.product import NonExistentProductException, NoPositivePriceException, NegativeProfitException
from model.repository.exc.sale import NoEnoughProductQuantityException, NonExistentSaleException, \
    ChangeProductIdInSaleException
from model.repository.factory import RepositoryFactory
from model.repository.sale import SaleFilter
from model.util.monetary_types import CUPMoney
from tests.util.general import TEST_DB_URL, delete_all_products_from_database, insert_product_and_return_it, \
    get_all_sales_from_database, assert_sale_lists_are_equal_ignoring_id, get_one_product_from_database, \
    insert_sale_and_return_it, get_one_sale_from_database, insert_products_in_database_and_return_them, \
    insert_sales_and_return_them
from tests.util.generators.product import ProductGenerator
from tests.util.generators.sale import SaleGenerator


class TestSaleRepository(unittest.TestCase):

    def setUp(self):
        self.sale_repository = RepositoryFactory.get_sale_repository(TEST_DB_URL)
        self.TODAY_DATE = date.today()

    def tearDown(self):
        RepositoryFactory.close_session()
        delete_all_products_from_database()

    def test_sales_are_inserted(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sale = SaleGenerator.generate_one_sale_from_product(product)

        self.sale_repository.insert_sales(sale, 3)

        inserted_sales = get_all_sales_from_database()
        correct_sales = [sale] * 3
        assert_sale_lists_are_equal_ignoring_id(inserted_sales, correct_sales)

    def test_sale_insertion_with_zero_quantity_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sale = SaleGenerator.generate_one_sale_from_product(product)

        self.assertRaises(ValueError, self.sale_repository.insert_sales, sale, 0)

    def test_sale_insertion_decreases_product_quantity(self):
        product = ProductGenerator.generate_one_product()
        product.quantity = 5
        product = insert_product_and_return_it(product)
        sale = SaleGenerator.generate_one_sale_from_product(product)

        self.sale_repository.insert_sales(sale, 3)

        product = get_one_product_from_database()
        self.assertEqual(product.quantity, 2)

    def test_sale_insertion_with_no_enough_products_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product.quantity = 2
        product = insert_product_and_return_it(product)
        sale = SaleGenerator.generate_one_sale_from_product(product)

        self.assertRaises(NoEnoughProductQuantityException, self.sale_repository.insert_sales, sale, 5)

    def test_sale_insertion_with_nonexistent_product_raises_exception(self):
        sale = SaleGenerator.generate_one_sale_without_product()
        nonexistent_product_id = 3
        sale.product_id = nonexistent_product_id

        self.assertRaises(NonExistentProductException, self.sale_repository.insert_sales, sale, 1)

    def test_sale_insertion_with_no_positive_price_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sale = SaleGenerator.generate_one_sale_from_product(product)
        sale.price = CUPMoney('0.00')

        self.assertRaises(NoPositivePriceException, self.sale_repository.insert_sales, sale, 1)

    def test_sale_insertion_with_negative_profit_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sale = SaleGenerator.generate_one_sale_from_product(product)
        sale.profit = CUPMoney('-1.00')

        self.assertRaises(NegativeProfitException, self.sale_repository.insert_sales, sale, 1)

    def test_sale_is_deleted_successfully(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sale = SaleGenerator.generate_one_sale_from_product(product)
        sale = insert_sale_and_return_it(sale)

        self.sale_repository.delete_sale(sale)

        read_sales = get_all_sales_from_database()
        self.assertEqual(read_sales, [])

    def test_trying_to_delete_nonexistent_sale_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sale = SaleGenerator.generate_one_sale_from_product(product)
        sale.id = 5

        self.assertRaises(NonExistentSaleException, self.sale_repository.delete_sale, sale)

    def test_delete_sale_with_nonexistent_product_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sale = SaleGenerator.generate_one_sale_from_product(product)
        sale = insert_sale_and_return_it(sale)
        sale.product_id = 10

        self.assertRaises(NonExistentProductException, self.sale_repository.delete_sale, sale)

    def test_sale_deleted_increases_associated_product_quantity(self):
        product = ProductGenerator.generate_one_product()
        product.quantity = 3
        product = insert_product_and_return_it(product)
        sale = SaleGenerator.generate_one_sale_from_product(product)
        sale = insert_product_and_return_it(sale)

        self.sale_repository.delete_sale(sale)

        product = get_one_product_from_database()
        self.assertEqual(product.quantity, 4)

    def test_sale_is_updated_successfully(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sale = SaleGenerator.generate_one_sale_from_product(product)
        new_sale = insert_sale_and_return_it(sale)

        new_sale.price = CUPMoney('50')
        new_sale.profit = CUPMoney('40')
        new_sale.date = new_sale.date - timedelta(days=1)
        self.sale_repository.update_sale(new_sale)

        read_sale = get_one_sale_from_database()
        self.assertEqual(new_sale, read_sale)

    def test_trying_to_update_nonexistent_sale_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sale = SaleGenerator.generate_one_sale_from_product(product)
        sale.id = 5

        self.assertRaises(NonExistentSaleException, self.sale_repository.update_sale, sale)

    def test_trying_to_change_product_of_a_sale_raises_exception(self):
        products = ProductGenerator.generate_products_by_quantity(2)
        product_1, product_2 = insert_products_in_database_and_return_them(products)
        sale = SaleGenerator.generate_one_sale_from_product(product_1)
        sale = insert_sale_and_return_it(sale)

        sale.product_id = product_2.id
        self.assertRaises(ChangeProductIdInSaleException, self.sale_repository.update_sale, sale)

    def test_sale_update_without_positive_price_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sale = SaleGenerator.generate_one_sale_from_product(product)
        sale = insert_sale_and_return_it(sale)

        sale.price = CUPMoney('0.00')
        self.assertRaises(NoPositivePriceException, self.sale_repository.update_sale, sale)

    def test_sale_update_with_negative_profit_raises_exception(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sale = SaleGenerator.generate_one_sale_from_product(product)
        sale = insert_sale_and_return_it(sale)

        sale.profit = CUPMoney('-1.00')
        self.assertRaises(NegativeProfitException, self.sale_repository.update_sale, sale)

    def test_all_sales_are_read_from_database(self):
        product = ProductGenerator.generate_one_product()
        product.quantity = 5
        product = insert_product_and_return_it(product)
        sales = SaleGenerator.generate_sales_from_product(product, 3)
        sales = insert_sales_and_return_them(sales)

        read_sales = self.sale_repository.get_all_sales()

        self.assertEqual(read_sales, sales)

    def test_get_sales_by_filter_using_date_range(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sales = SaleGenerator.generate_sales_from_product(product, 3)
        s1, s2, s3 = sales
        one_day, two_days = timedelta(days=1), timedelta(days=2)
        s1.date = self.TODAY_DATE
        s2.date = self.TODAY_DATE + one_day
        s3.date = self.TODAY_DATE + two_days
        sales = insert_sales_and_return_them(sales)

        sale_filter = SaleFilter()
        sale_filter.minimum_date = self.TODAY_DATE
        sale_filter.maximum_date = self.TODAY_DATE + two_days
        filtered_sales = self.sale_repository.get_sales_by_filter(sale_filter)

        self.assertEqual(filtered_sales, sales)

    def test_get_sales_by_using_product_id_list(self):
        products = ProductGenerator.generate_products_by_quantity(3)
        products = insert_products_in_database_and_return_them(products)
        p1, p2, p3 = products
        sales_of_p1 = SaleGenerator.generate_sales_from_product(p1, 2)
        sales_of_p2 = SaleGenerator.generate_sales_from_product(p2, 2)
        sales_of_p3 = SaleGenerator.generate_sales_from_product(p3, 2)
        sales_of_p1 = insert_sales_and_return_them(sales_of_p1)
        sales_of_p2 = insert_sales_and_return_them(sales_of_p2)
        sales_of_p3 = insert_sales_and_return_them(sales_of_p3)

        sale_filter = SaleFilter()
        sale_filter.product_id_list = [p1.id, p3.id]
        filtered_sales = self.sale_repository.get_sales_by_filter(sale_filter)

        sales_of_p1_and_p3 = sales_of_p1 + sales_of_p3
        self.assertEqual(filtered_sales, sales_of_p1_and_p3)

    def test_get_sales_by_filter_using_sale_ids(self):
        product = ProductGenerator.generate_one_product()
        product = insert_product_and_return_it(product)
        sales = SaleGenerator.generate_sales_from_product(product, 3)
        s1, s2, s3 = sales
        insert_sales_and_return_them(sales)

        filter_by_id = SaleFilter()
        filter_by_id.sale_id_list = [s1.id, s3.id]
        filtered_sales = self.sale_repository.get_sales_by_filter(filter_by_id)

        self.assertEqual(filtered_sales, [s1, s3])
