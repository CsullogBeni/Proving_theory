from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets

from Model.model import Model


class AxiomDialog(QDialog):
    """
    AxiomDialog is initialized when the user want to use the axiom rule and wants to substitute a formula into
    an axiom. This dialog contains buttons, with the base axioms, or the added axioms based on which function called.

    Attributes:
        __layout: (QVBoxLayout) vertical layout contain the buttons.
        axiom: (str) axiom, that will be used by the user.
        data: (str list) contains the formulas, that will be substituted into the axiom
    """

    def __init__(self) -> None:
        """
        Constructor for the AxiomDialog. Initialize the variables.
        """
        super(AxiomDialog, self).__init__()
        self.setWindowTitle('Pick an axiom!')
        self.__layout = QtWidgets.QVBoxLayout(self)
        self.data = []
        self.axiom = None

    def add_data(self, model: Model, base_axioms: bool = True) -> None:
        """
        Fulfill the layout with buttons. Run through the model's base or added axioms and bind every
        formula to a button.
        The function places a cancel button to the dialog as well.

        Args:
            model: current model, the model's base/added axioms in use
            base_axioms: decides that the base or the added axioms will be used
        """
        from View.Utils.utils import text_formatter
        if not isinstance(model, Model):
            return
        buttons = []
        if base_axioms:
            for idx, formula in enumerate(model.base_axioms):
                buttons.append(QtWidgets.QPushButton(text_formatter(str(idx + 1) + '. ' + str(formula)), self))
                buttons[idx].clicked.connect(lambda _, f=formula: self.__try_axiom(f))
                buttons[idx].setFixedWidth(500)
                self.__layout.addWidget(buttons[idx])
        else:
            if len(model.added_axioms) == 0:
                msg_box = QtWidgets.QMessageBox()
                msg_box.setWindowTitle('Warning')
                msg_box.setText("There is no added axioms!")
                msg_box.exec_()
                self.close()
                return
            else:
                for idx, formula in enumerate(model.added_axioms):
                    buttons.append(QtWidgets.QPushButton(
                        text_formatter(str(idx + 1 + len(model.base_axioms)) + '. ' + str(formula)), self))
                    buttons[idx].clicked.connect(lambda _, f=formula: self.__try_axiom(f))
                    buttons[idx].setFixedWidth(500)
                    self.__layout.addWidget(buttons[idx])

        buttons.append(QtWidgets.QPushButton('Cancel'))
        buttons[len(buttons) - 1].clicked.connect(self.close)
        self.__layout.addWidget(buttons[len(buttons) - 1])
        self.setLayout(self.__layout)

    def __try_axiom(self, formula: str) -> None:
        """
        Sets which axiom is in use and tuns through the axiom's all logical variables and raises an QInputDialog
        where the user can type the formulas that will be substituted into the axiom.
        Args:
            formula: the logical axiom
        """
        from Model.Utils.utils import Utils
        self.axiom = formula
        variables = Utils.get_formula_variables(formula)
        for idx, var in enumerate(variables):
            replace_var, dialog = QtWidgets.QInputDialog.getText(self, 'Input Dialog', str(var) + ': ')
            if dialog:
                self.data.append(replace_var)
        self.close()
