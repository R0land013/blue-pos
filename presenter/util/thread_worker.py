from PyQt5.QtCore import pyqtSignal, QThread


class PresenterThreadWorker(QThread):

    when_initialized = pyqtSignal()
    when_finished = pyqtSignal()

    def __init__(self, a_callable):
        super().__init__()
        self.__a_callable = a_callable

    def run(self):
        self.when_initialized.emit()
        self.__a_callable()
        self.when_finished.emit()

