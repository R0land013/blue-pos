from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt, QLocale

class CUPSpinBox(QDoubleSpinBox):

    def __init__(self, minimum: float, maximum: float, value: float):
        super().__init__()

        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.setValue(value)

        self.setSuffix(' CUP')
        self.setDecimals(2)
        self.setSingleStep(10.00)
        
        # De este modo el separador entre la parte entera y decimal siempre será
        # un punto, y no la coma. Aquí se fuerza porque puede variar dependiendo
        # de la ubicación que tenga el Sistema Operativo
        self.setLocale(QLocale(QLocale.Language.Spanish, QLocale.Country.UnitedStates))

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Comma or event.key() == Qt.Key.Key_Plus:
            return
        
        super().keyPressEvent(event)