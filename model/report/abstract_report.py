from pathlib import Path


class AbstractSaleReport:

    def get_sales(self) -> list:
        raise NotImplementedError()

    def generate_report_as_html(self, path: Path):
        raise NotImplementedError()

    def generate_report_as_pdf(self, path: Path):
        raise NotImplementedError()
