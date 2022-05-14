from datetime import date
from model.report.abstract_report import AbstractSaleReport
from model.repository.sale import SaleRepository


class DaySaleReport(AbstractSaleReport):

    def __init__(self, day_date: date, repository: SaleRepository):
        raise NotImplementedError()
