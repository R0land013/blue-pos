from datetime import date, timedelta
from sqlalchemy import select, cast, FLOAT
from sqlalchemy.orm import Session, aliased
from typing import List
from model.entity.models import Product, Sale
from model.report.sales_grouped_by_product import SalesGroupedByProduct
from sqlalchemy import func

from model.util.monetary_types import CUPMoney


class SalesGroupedByProductRepository:

    def __init__(self, session: Session):
        self.__session: Session = session

    def get_groups_on_week(self, week_date: date) -> List[SalesGroupedByProduct]:
        monday_date = week_date - timedelta(days=week_date.weekday())
        sunday_date = week_date + timedelta(days=6 - week_date.weekday())
        query = self.__construct_query_using_date_limits(monday_date, sunday_date)
        rows = self.__session.execute(query).all()
        return self.__construct_sale_groups_from_result(rows, monday_date, sunday_date)

    @staticmethod
    def __construct_query_using_date_limits(initial_date: date, final_date: date):
        acquired_money = func.sum(cast(Sale.price, FLOAT)).label('acquired_money')
        total_cost = func.sum(cast(Sale.cost, FLOAT)).label('total_cost')
        sale_quantity = func.count(Sale.id).label('sale_quantity')
        query = select(Product.id, Product.name, acquired_money, total_cost, sale_quantity)\
            .join(Sale, Product.id == Sale.product_id)\
            .where(Sale.date >= initial_date)\
            .where(Sale.date <= final_date)\
            .group_by(Sale.product_id)
        return query

    @staticmethod
    def __construct_sale_groups_from_result(rows, initial_date: date, final_date: date) -> List[SalesGroupedByProduct]:
        groups = []
        for a_row in rows:
            acquired_money = CUPMoney(str(a_row['acquired_money']))
            total_cost = CUPMoney(str(a_row['total_cost']))
            total_profit = acquired_money - total_cost
            groups.append(SalesGroupedByProduct(
                product_id=a_row[0],
                product_name=a_row[1],
                acquired_money=acquired_money,
                total_cost=total_cost,
                total_profit=total_profit,
                sale_quantity=a_row[4],
                initial_date=initial_date,
                final_date=final_date
            ))
        return groups

    def get_groups_on_month(self, month_date: date) -> List[SalesGroupedByProduct]:
        pass

    def get_groups_on_year(self, year_date: date) -> List[SalesGroupedByProduct]:
        pass
