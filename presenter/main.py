from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent
from sqlalchemy import create_engine
from model.entity.models import Base
from model.repository.factory import DB_URL
from presenter.product_management import ProductManagementPresenter
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
