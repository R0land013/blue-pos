from pathlib import Path
from model.report.abstract_report import AbstractSaleReport


def generate_html_file(file_path: Path, report: AbstractSaleReport):
    with file_path.open(mode='w') as file:
        file.write(report.get_report_as_html())
