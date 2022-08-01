from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent
from sqlalchemy import create_engine
from model.entity.models import Base
from model.repository.factory import DB_URL
from presenter.day_report import DaySaleReportPresenter
from presenter.month_report import MonthSaleReportPresenter
from presenter.product_management import ProductManagementPresenter
from presenter.week_report import WeekSaleReportPresenter
from presenter.year_report import YearSaleReportPresenter
from view.main import MainView


class MainPresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__initialize_view()
        self.__create_database()

    def __initialize_view(self):
        view = MainView(self)
        self._set_view(view)

    @staticmethod
    def __create_database():
        engine = create_engine(DB_URL, future=True)
        Base.metadata.create_all(engine)

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
