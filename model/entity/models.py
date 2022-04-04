from sqlalchemy.orm import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

Base = declarative_base()


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=80), nullable=False, unique=True)
    description = Column(String(length=300), nullable=True, default='')
