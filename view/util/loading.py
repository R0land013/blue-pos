from PyQt5.QtCore import Qt, QPropertyAnimation, QAbstractAnimation, QPoint, QEvent
from PyQt5.QtGui import QMovie, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsOpacityEffect
from util.resources_path import resource_path


class LoadingAnimation(QWidget):

    def __init__(self, parent=None, message='Cargando'):
        super().__init__(parent)
        self.__message = message
        self.__parent = parent

        self.__setup_view()
        self.__setup_animation()

        parent.installEventFilter(self)
        self.installEventFilter(self)

    def __setup_view(self):
        self.__loading_movie = QMovie(resource_path('view/ui/images/loading.gif'))
        self.__movie_label = QLabel()
        self.__movie_label.setObjectName('movie_label')
        self.__movie_label.setMovie(self.__loading_movie)
        self.__movie_label.setScaledContents(True)

        self.__label = QLabel(self.__message)
        self.__label.setObjectName('loading_message_label')
        self.__label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.__label.setStyleSheet(
            """
            QLabel#loading_message_label{
                color: black;
                font-family: Arial;
                font-weight: bold;
                font: 15pt;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                background-color: #C6F0FF;
            }
            """)
        self.setStyleSheet(
            """
            QLabel#movie_label{
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                background-color: #C6F0FF;
            }
            """)

        layout = QVBoxLayout()
        layout.addWidget(self.__movie_label)
        layout.addWidget(self.__label)
        layout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.setMinimumWidth(400)
        self.setMinimumHeight(400)

    def __setup_animation(self):

        self.__animation = QPropertyAnimation(self, b"opacity")
        self.__animation.setStartValue(0.0)
        self.__animation.setDuration(200)
        self.__animation.setEndValue(1.0)
        self.__animation.valueChanged.connect(self.__set_opacity)
        self.setGraphicsEffect(QGraphicsOpacityEffect(opacity=0.0))

    def __set_opacity(self, opacity: float):
        opacity_effect = QGraphicsOpacityEffect(opacity=opacity)
        self.setGraphicsEffect(opacity_effect)

    def show(self):
        self.__set_on_center_position()
        self.__animation.setDirection(QAbstractAnimation.Forward)
        self.__animation.start()
        self.__loading_movie.start()
        self.raise_()
        super().show()

    def __set_on_center_position(self):
        geometry = self.geometry()
        geometry.moveCenter(QPoint(self.__parent.rect().center().x(), self.__parent.rect().center().y()))
        self.setGeometry(geometry)

    def hide(self):
        if self.__animation.state() == QPropertyAnimation.Running:
            self.__animation.stop()

        self.__animation.setDirection(QAbstractAnimation.Backward)
        self.__animation.start()
        self.__loading_movie.stop()
        super().hide()

    def eventFilter(self, obj, e) -> bool:
        if e.type() == QEvent.Resize:
            self.__set_on_center_position()
        return super().eventFilter(obj, e)


class LoadingView(QWidget):

    loading_animation: LoadingAnimation = None

    def show_loading_with_message(self, message: str):
        self.loading_animation = LoadingAnimation(parent=self, message=message)
        self.setDisabled(True)
        self.loading_animation.show()

    def hide_loading_animation(self):
        if self.loading_animation is None:
            raise Exception('Not running loading animation.')

        self.loading_animation.hide()
        self.setDisabled(False)
