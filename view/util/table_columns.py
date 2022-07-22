from PyQt5.QtWidgets import QTableWidgetItem
from model.util.monetary_types import CUPMoney


class QCustomTableItemTypes:

    CUP_MONEY_TYPE = 1000
    INTEGER_TYPE = 1001


class QCUPMoneyTableItem(QTableWidgetItem):

    def __init__(self, text: str):
        super().__init__(text, type=QCustomTableItemTypes.CUP_MONEY_TYPE)

    def __lt__(self, other):
        this_money = CUPMoney(self.text().split()[1])
        other_money = CUPMoney(other.text().split()[1])
        return this_money < other_money


class QIntegerTableItem(QTableWidgetItem):

    def __init__(self, text: str):
        super().__init__(text, type=QCustomTableItemTypes.INTEGER_TYPE)

    def __lt__(self, other):
        this_integer = int(self.text())
        other_integer = int(other.text())
        return this_integer < other_integer
