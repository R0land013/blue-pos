from model.entity.models import Base
from sqlalchemy import create_engine
from pathlib import Path


def set_up():
    engine = create_engine("sqlite:///test.db", future=True)
    Base.metadata.create_all(engine)


def tear_down():
    db_file = Path('test.db')
    if db_file.exists():
        db_file.unlink()
