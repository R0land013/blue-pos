from pathlib import Path

from model.entity.models import Base
from sqlalchemy import create_engine

from tests.util.general import TEST_REPORT_PATH


def __delete_test_database():
    db_file = Path('test.db')
    if db_file.exists():
        db_file.unlink()


def __create_generated_report_folder():
    if not TEST_REPORT_PATH.exists():
        TEST_REPORT_PATH.mkdir(parents=True)


def set_up():
    __create_generated_report_folder()
    __delete_test_database()

    engine = create_engine("sqlite:///test.db", future=True)
    Base.metadata.create_all(engine)


def tear_down():
    __delete_test_database()
