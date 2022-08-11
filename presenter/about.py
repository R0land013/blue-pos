from easy_mvp.abstract_presenter import AbstractPresenter

from view.about import AboutView


class AboutPresenter(AbstractPresenter):

    def _on_initialize(self):
        self._set_view(AboutView(self))

    def close_presenter(self):
        self._close_this_presenter()
