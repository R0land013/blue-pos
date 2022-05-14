from datetime import date
from model.report.abstract_report import AbstractSaleReport


class DaySaleReport(AbstractSaleReport):

    def __init__(self, day_date: date):
        raise NotImplementedError()
