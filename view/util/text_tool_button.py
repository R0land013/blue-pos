from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QFrame


class ToolButtonWithTextAndIcon(QFrame):

    clicked = pyqtSignal()

    def __init__(self, text: str):
        super().__init__()

        self.__image_label = QLabel()
        self.__label = QLabel(text)

        self.__setup_gui()
        self.__set_gui_style()

    def set_icon(self, pixmap: QPixmap):
        self.__image_label.setPixmap(pixmap)
        self.__image_label.setScaledContents(True)

    def __setup_gui(self):
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.__image_label, 0, Qt.AlignCenter)
        self.layout().addWidget(self.__label, 0, Qt.AlignCenter)
        self.setMouseTracking(True)

    def __set_gui_style(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.setCursor(Qt.PointingHandCursor)
        self.__image_label.setMaximumSize(30, 30)
        self.__label.setStyleSheet(
            """
            font: 8pt;
            padding: 0;
            """)

    def setDisabled(self, disabled: bool):
        # Se resetean los estilos
        self.setStyleSheet('')
        self.__label.setStyleSheet('font: 8pt;')
        super().setDisabled(disabled)

    def mouseReleaseEvent(self, mouse_event: QMouseEvent):
        if self.underMouse() and mouse_event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

    def enterEvent(self, event) -> None:
        if self.isEnabled():
            self.setStyleSheet(
                """
                background-color: #CCE9FF;
                border-radius: 10px;
                """)
            self.__label.setStyleSheet(
                """
                font: 8pt;
                background-color: #CCE9FF;
                """)

    def leaveEvent(self, event):
        self.setStyleSheet(
            """
            background-color: white;
            """)
        self.__label.setStyleSheet(
            """
            font: 8pt;
            background-color: white;
            """)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.__set_clicked_style()

    def __set_clicked_style(self):
        self.setStyleSheet(
            """
            background-color: #B0D3FF;
            border-radius: 10px;
            """)
        self.__label.setStyleSheet(
            """
            font: 8pt;
            background-color: #B0D3FF;
            """)
