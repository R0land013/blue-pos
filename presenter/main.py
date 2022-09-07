from PyQt5.QtWidgets import QApplication
from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent
from sqlalchemy import create_engine
from model.entity.models import Base
from model.repository.factory import DB_URL
from presenter.about import AboutPresenter
from presenter.custom_report import CustomSaleReportPresenter
from presenter.day_report import DaySaleReportPresenter
from presenter.expense_management import ExpenseManagementPresenter
from presenter.month_report import MonthSaleReportPresenter
from presenter.product_management import ProductManagementPresenter
from presenter.week_report import WeekSaleReportPresenter
from presenter.year_report import YearSaleReportPresenter
from presenter.year_statistics import YearStatisticsPresenter
from view.main import MainView


class MainPresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__initialize_view()
        self.__create_database()
        self.__set_app_style()

    def __initialize_view(self):
        view = MainView(self)
        self._set_view(view)

    @staticmethod
    def __create_database():
        engine = create_engine(DB_URL, future=True)
        Base.metadata.create_all(engine)

    @staticmethod
    def __set_app_style():
        with open('./view/style/blue.qss', 'r') as f:
            style = f.read()
            QApplication.instance().setStyleSheet(style)

    def get_default_window_title(self) -> str:
        return 'Blue POS'

    def open_product_management(self):
        intent = Intent(ProductManagementPresenter)
        self._open_other_presenter(intent)

    def open_day_sale_report_presenter(self):
        intent = Intent(DaySaleReportPresenter)
        self._open_other_presenter(intent)

    def open_month_sale_report_presenter(self):
        intent = Intent(MonthSaleReportPresenter)
        self._open_other_presenter(intent)

    def open_year_sale_report_presenter(self):
        intent = Intent(YearSaleReportPresenter)
        self._open_other_presenter(intent)

    def open_week_sale_report_presenter(self):
        intent = Intent(WeekSaleReportPresenter)
        self._open_other_presenter(intent)

    def open_custom_sale_report_presenter(self):
        intent = Intent(CustomSaleReportPresenter)
        self._open_other_presenter(intent)

    def open_about_presenter(self):
        intent = Intent(AboutPresenter)
        self._open_other_presenter(intent)

    def open_expense_management_presenter(self):
        intent = Intent(ExpenseManagementPresenter)
        self._open_other_presenter(intent)

    def open_year_statistics_presenter(self):
        intent = Intent(YearStatisticsPresenter)
        self._open_other_presenter(intent)
