from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from model.util.money_colum import MoneyColumn
from model.util.monetary_types import CUPMoney
from datetime import date

Base = declarative_base()


class Product(Base):

    def __repr__(self):
        return '[id: {}, name: "{}", description: "{}", price: {}, profit: {}, ' \
               'quantity: {}]'.format(self.id, self.name, self.description, self.price,
                                      self.profit, self.quantity)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return (self.id == other.id and self.name == other.name and self.description == other.description
                and self.price == other.price and self.profit == other.profit
                and self.quantity == other.quantity)

    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=80), nullable=False, unique=True)
    description = Column(String(length=300), nullable=True, default='')
    price = Column(MoneyColumn(), nullable=False, default=CUPMoney('1.00'))
    profit = Column(MoneyColumn(), nullable=False, default=CUPMoney('1.00'))
    quantity = Column(Integer, nullable=False, default=0)


class Sale(Base):

    def __repr__(self):
        return 'Sale(id: {}, product_id: "{}", date: "{}", price: {}, profit: {})'\
            .format(self.id, self.product_id, self.date, self.price, self.profit)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return (self.id == other.id and self.product_id == other.product_id
                and self.date == other.date and self.price == other.price
                and self.profit == other.profit)

    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    date = Column(Date, nullable=False, default=date.today())
    price = Column(MoneyColumn(), nullable=False, default=CUPMoney('1.00'))
    profit = Column(MoneyColumn(), nullable=False, default=CUPMoney('1.00'))
    product = relationship('Product', backref=backref('sales', cascade='all,delete'))
