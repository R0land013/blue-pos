from PyQt5.QtWidgets import QWidget, QMessageBox


class ErrorView(QWidget):

    def show_error_message(self, message, title='Error'):
        QMessageBox.critical(self.window(), title, message)