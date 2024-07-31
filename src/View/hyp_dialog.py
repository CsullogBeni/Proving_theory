from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets

from Model.model import Model


class HypDialog(QDialog):
    """
    HipDialog is initialized when the user want to use the hypothesis rule. This dialog contains buttons, with
    the formulas in the formula set, and a cancel button for returning.

    Attributes:
        __layout: (QVBoxLayout) vertical layout contain the buttons.
        hyp: (str) contains the chosen formula from the formula set
    """

    def __init__(self) -> None:
        """
        Constructor for the HipDialog. Initialize the variables.
        """
        super(HypDialog, self).__init__()
        self.setWindowTitle('Pick a hypothesis!')
        self.__layout = QtWidgets.QVBoxLayout(self)
        self.hyp = None

    def add_data(self, model: Model) -> None:
        """
        Fulfill the layout with buttons. Run through the model's formula set and bind every formula to a button.
        The function places a cancel button to the dialog as well.

        Args:
            model: current model, contains the formula set
        """
        from View.Utils.utils import text_formatter
        if not isinstance(model, Model):
            return

        buttons = []
        for idx, formula in enumerate(model.formula_set):
            buttons.append(QtWidgets.QPushButton(text_formatter(str(formula)), self))
            buttons[idx].clicked.connect(lambda _, f=formula: self.__try_hyp(f))
            buttons[idx].setFixedWidth(300)
            self.__layout.addWidget(buttons[idx])

        buttons.append(QtWidgets.QPushButton('Cancel'))
        buttons[len(buttons) - 1].clicked.connect(self.close)
        self.__layout.addWidget(buttons[len(buttons) - 1])
        self.setLayout(self.__layout)
        self.hyp = 'Cancel'

    def __try_hyp(self, formula: str) -> None:
        """
        Function binded to the buttons, sets the hip variable as the chosen formula.
        Args:
            formula: the chosen formula, that will be added to the steps.
        """
        self.hyp = formula
        self.close()
