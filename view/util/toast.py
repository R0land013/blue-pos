from PyQt5.QtWidgets import QWidget
from pyqt_toast import Toast


class ToastView(QWidget):

    def show_green_toast_message(self, message: str, duration: int = 2):
        toast = Toast(message, duration=duration, parent=self)
        toast.setBackgroundColor('#21C200')
        toast.setForegroundColor('#FFFFFF')
        toast.setOpacity(1.0)

        toast.show()
