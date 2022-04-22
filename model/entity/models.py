from sqlalchemy.orm import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from model.util.money_colum import MoneyColumn
from money import Money

Base = declarative_base()


class Product(Base):

    def __repr__(self):
        return '[id: {}, name: "{}", description: "{}"]'.format(self.id, self.name, self.description)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.description == other.description

    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=80), nullable=False, unique=True)
    description = Column(String(length=300), nullable=True, default='')
    price = Column(MoneyColumn(), nullable=False, default=Money('1.00', 'CUP'))
    profit = Column(MoneyColumn(), nullable=False, default=Money('1.00', 'CUP'))
    quantity = Column(Integer, nullable=False, default=0)
