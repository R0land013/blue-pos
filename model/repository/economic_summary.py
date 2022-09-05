from datetime import date
from sqlalchemy.orm import Session
from model.entity.economic_summary import EconomicSummary


class EconomicSummaryRepository:

    def __init__(self, session: Session):
        pass

    def get_economic_summary_on_month(self, month_date: date) -> EconomicSummary:
        pass
