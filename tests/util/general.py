from sqlalchemy.orm import Session
from sqlalchemy import create_engine

TEST_DB_URL = 'sqlite:///test.db'


def create_test_session() -> Session:
    engine = create_engine(TEST_DB_URL)
    return Session(engine)
