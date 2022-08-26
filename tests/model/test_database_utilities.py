import sqlite3
from unittest import TestCase
from pathlib import Path
from model.database_utilities import backup_database, restore_database


class TestDatabaseUtilities(TestCase):

    TEST_UTILITY_DATABASE_PATH = 'test_database_utility.db'
    BACKUP_FILE_PATH = 'backup_file.db'

    def setUp(self):
        self.delete_database_and_backup_files()
        self.create_database_for_tests()

    def create_database_for_tests(self):
        self.connection = self.get_database_connection()
        self.connection.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT NOT NULL)')
        self.connection.close()

    def delete_database_and_backup_files(self):
        test_db_path = Path(self.TEST_UTILITY_DATABASE_PATH)
        if test_db_path.exists():
            test_db_path.unlink()

        backup_file_path = Path(self.BACKUP_FILE_PATH)
        if backup_file_path.exists():
            backup_file_path.unlink()

    def get_database_connection(self):
        return sqlite3.connect(self.TEST_UTILITY_DATABASE_PATH)

    def tearDown(self):
        self.delete_database_and_backup_files()

    def test_backup_and_restore_database(self):
        self.insert_a_product_into_database()

        backup_database(self.TEST_UTILITY_DATABASE_PATH, self.BACKUP_FILE_PATH)
        self.delete_all_from_database()
        restore_database(self.TEST_UTILITY_DATABASE_PATH, self.BACKUP_FILE_PATH)

        names_in_database = self.get_all_product_names_from_database()
        self.assertEqual(names_in_database, ['chair'])

    def insert_a_product_into_database(self):
        connection = self.get_database_connection()
        connection.execute('INSERT INTO products VALUES(1, "chair")')
        connection.commit()
        connection.close()

    def delete_all_from_database(self):
        connection = self.get_database_connection()
        connection.execute('DELETE FROM products')
        connection.commit()
        connection.close()

    def get_all_product_names_from_database(self) -> list:
        connection = self.get_database_connection()
        rows = connection.execute('SELECT name FROM products')
        names = list(map(lambda a_row: a_row[0], rows))
        connection.close()
        return names
