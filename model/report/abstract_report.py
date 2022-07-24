from model.report.statistics import ReportStatistic


class AbstractSaleReport:

    def get_sales(self) -> list:
        raise NotImplementedError()

    def get_report_as_html(self) -> str:
        raise NotImplementedError()

    def get_report_statistics(self) -> ReportStatistic:
        raise NotImplementedError()
