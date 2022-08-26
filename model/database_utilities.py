import sqlite3
from pathlib import Path
import shutil


def backup_database(database_path: str, backup_path: str):
    database_connection = sqlite3.connect(database_path)
    backup_connection = sqlite3.connect(backup_path)
    database_connection.backup(backup_connection)

    database_connection.close()
    backup_connection.close()


def restore_database(database_path: str, backup_path: str):
    working_database_path = Path(database_path)
    backup_database_path = Path(backup_path)
    shutil.copy(backup_database_path.absolute(), working_database_path.absolute())
