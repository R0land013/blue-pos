from datetime import date
from typing import Tuple
from sqlalchemy.orm import Session
from model.entity.economic_summary import EconomicSummary


class EconomicSummaryRepository:

    def __init__(self, session: Session):
        pass

    def get_economic_summaries_by_month_on_year(self, year_date: date) -> Tuple[EconomicSummary]:
        pass
