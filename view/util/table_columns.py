from PyQt5.QtWidgets import QTableWidgetItem
from model.util.monetary_types import CUPMoney


class QCustomTableItemTypes:

    CUP_MONEY_TYPE = 1000
    INTEGER_TYPE = 1001


class QCUPMoneyTableItem(QTableWidgetItem):

    def __init__(self, text: str):
        super().__init__(text, type=QCustomTableItemTypes.CUP_MONEY_TYPE)

    def __lt__(self, other):
        this_amount_str = self.text().split()[1]
        other_amount_str = other.text().split()[1]
        this_money = self.__create_cup_money(this_amount_str)
        other_money = self.__create_cup_money(other_amount_str)
        return this_money < other_money

    @staticmethod
    def __create_cup_money(cell_text: str):
        # CUPMoney usa comas para separar tres lugares en los números
        # cuando se imprimen. Por esta razón es necesario eliminar las comas
        # de el número para crear el objeto Money. Ejemplo: CUPMoney('1,000.00')
        # es incorrecto.  La manera correcta es CUPMoney('1000.00'), sin comas.
        return CUPMoney(''.join(cell_text.split(',')))


class QIntegerTableItem(QTableWidgetItem):

    def __init__(self, text: str):
        super().__init__(text, type=QCustomTableItemTypes.INTEGER_TYPE)

    def __lt__(self, other):
        this_integer = int(self.text())
        other_integer = int(other.text())
        return this_integer < other_integer
