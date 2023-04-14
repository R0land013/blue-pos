from pathlib import Path
from model.report.abstract_report import AbstractSaleReport
from xhtml2pdf import pisa
import os

class DirectoryPermissionError(Exception):

    def __init__(self, path: str):
        super().__init__(f'User does not have permission to write or read in path {path}')
        self.__path = path
    
    @property
    def path(self):
        return self.__path

def __user_has_access_to_write_file(path: Path):
    base_path, file_name = os.path.split(str(path.absolute()))
    
    if not os.access(base_path, os.W_OK or os.R_OK):
        raise DirectoryPermissionError(base_path)
    
    return True

def generate_html_file(file_path: Path, report: AbstractSaleReport):
    if __user_has_access_to_write_file(file_path):
        with file_path.open(mode='w') as file:
            file.write(report.get_report_as_html())


def generate_pdf_file(file_path: Path, report: AbstractSaleReport):
    if __user_has_access_to_write_file(file_path):
        with file_path.open('w+b') as pdf_file:
            pisa.CreatePDF(report.get_report_as_html(), dest=pdf_file)
