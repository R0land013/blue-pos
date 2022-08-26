from datetime import date
from sqlalchemy.orm import Session
from typing import List
from model.report.sales_grouped_by_product import SalesGroupedByProduct


class SalesGroupedByProductRepository:

    def __init__(self, session: Session):
        self.__session: Session = session

    def get_groups_by_day_on_week(self, week_date: date) -> List[SalesGroupedByProduct]:
        pass

    def get_groups_by_day_on_month(self, month_date: date) -> List[SalesGroupedByProduct]:
        pass

    def get_groups_by_month_on_year(self, year_date: date) -> List[SalesGroupedByProduct]:
        pass
