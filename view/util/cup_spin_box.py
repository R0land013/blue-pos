from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt

class CUPSpinBox(QDoubleSpinBox):

    def __init__(self, minimum: float, maximum: float, value: float):
        super().__init__()

        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.setValue(value)

        self.setSuffix(' CUP')
        self.setDecimals(2)
        self.setSingleStep(10.00)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Comma or event.key() == Qt.Key.Key_Plus:
            return
        
        super().keyPressEvent(event)