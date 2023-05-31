import unittest
from model.repository.business_currency import BusinessCurrencyRepository
from model.entity.models import BusinessCurrency
from model.repository.factory import RepositoryFactory
from tests.util.general import create_test_session, TEST_DB_URL, delete_all_business_currency_from_database, insert_business_currency_and_return_it, get_all_business_from_database


class TestBusinessCurrencyRepository(unittest.TestCase):

    def setUp(self):
        self.session = create_test_session()
        self.repo = RepositoryFactory.get_business_currency_repository(
            TEST_DB_URL)

    def tearDown(self) -> None:
        delete_all_business_currency_from_database()
        RepositoryFactory.close_session()

    def test_exists_business_currency_returns_true_if_currency_exists(self):
        insert_business_currency_and_return_it(
            BusinessCurrency(currency_code='USD'))

        self.assertTrue(self.repo.exists_business_currency())

    def test_exists_business_currency_returns_false_if_no_currency_exists(self):
        self.assertFalse(self.repo.exists_business_currency())

    def test_set_business_currency_creates_new_currency_if_none_exists(self):
        self.repo.set_business_currency('USD')
        currencies = get_all_business_from_database()
        self.assertEqual(len(currencies), 1)
        self.assertEqual(currencies[0].currency_code, 'USD')

    def test_set_business_currency_updates_existing_currency(self):
        insert_business_currency_and_return_it(BusinessCurrency(currency_code='EUR'))

        self.repo.set_business_currency('USD')
        currencies = self.session.query(BusinessCurrency).all()
        self.assertEqual(len(currencies), 1)
        self.assertEqual(currencies[0].currency_code, 'USD')
