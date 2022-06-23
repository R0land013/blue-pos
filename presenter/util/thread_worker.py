from PyQt5.QtCore import pyqtSignal, QThread


class PresenterThreadWorker(QThread):

    when_started = pyqtSignal()
    when_finished = pyqtSignal()
    error_found = pyqtSignal(Exception)
    finished_without_error = pyqtSignal()

    def __init__(self, a_callable):
        super().__init__()
        self.__a_callable = a_callable

    def run(self):
        self.when_started.emit()
        self.__a_callable(self)
        self.when_finished.emit()

