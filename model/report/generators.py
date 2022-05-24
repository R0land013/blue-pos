from pathlib import Path
from model.report.abstract_report import AbstractSaleReport
from xhtml2pdf import pisa


def generate_html_file(file_path: Path, report: AbstractSaleReport):
    with file_path.open(mode='w') as file:
        file.write(report.get_report_as_html())


def generate_pdf_file(file_path: Path, report: AbstractSaleReport):
    with file_path.open('w+b') as pdf_file:
        pisa.CreatePDF(report.get_report_as_html(), dest=pdf_file)
