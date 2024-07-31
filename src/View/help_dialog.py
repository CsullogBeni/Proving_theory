from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont


class HelpDialog(QDialog):
    """
    This class for helping the user, show a string with helpful examples. Using the Dialog in the
    new_proving_method_config.py file.
    Attributes:
        __layout: The vertical layout of the HelpDialog
        __help_label: The HelpDialog will contain this label
        __close_button: The button on the HelpDialog, which closes it
    """
    def __init__(self, config=True):
        """
        Constructor for the HipDialog. Initialize the layouts and variables, such as the help label that
        contains a string, and a button that can close the QDialog.
        """
        super(HelpDialog, self).__init__()
        self.setWindowTitle('Help')

        self.__layout = QtWidgets.QVBoxLayout()
        if config:
            help_text = \
                """
                Formula set requires a list of logical formulas, can be empty. You must give one consequence formula.  
                Youcan type formulas in the first box.
                Use only these capital letters as variables: A, B, C, D, F, G, H, J, K, L, M, W, R, T, Z, U
                You must use capital letters. For typing logical formulas you can use this symbols:
                \t- '>>' as implication        
                \t- '|' as disjunction        
                \t- '&' as conjunction        
                \t- '~' as negation
                Formulas must be valid logical formulas, and it accepts fully and correctly closed parentheses formulas!
                Some examples:
                (A >> B)\t\t\t<=>\t\t(A ⊃ B)
                (A | B)\t\t\t\t<=>\t\t(A ∨ B)
                (A & B)\t\t\t<=>\t\t(A ∧ B)
                ~A\t\t\t\t<=>\t\t¬A
                (A >> (~B | (C & D)))\t\t<=>\t\t(A ⊃ (¬B ∨ (C ∧ D))) 
                """
        else:
            help_text = \
                """
                This window stands for simulating a proving theory deduction. There are 3 main rules, that you can use:
                \t1. HYP - hypothesis, you can choose a formula, from the formula set
                \t2. AXIOM - using an axiom from the base axioms, and replacing it's variables with logical formulas
                \t3. Using syntax rules, such as:
                \t\tMP - Modus Ponens rule : {A ⊃ B, A} |- B 
                \t\tMT - Modus Tollens rule : {A ⊃ B, ¬B} |- ¬A
                \t\tMTP - Modus Tollendo Ponens rule : {A ∨ B, ¬A} |- B
                \t\tMPT - Modus Ponendo Tollens rule : {¬A ⊃ ¬B, B} |- A
                \t\tCS - Conditional Syllogism rule : {A ⊃ B, B ⊃ C} |- A ⊃ C
                You can add axioms, but when you are typing the axioms, use this operators:
                \t- '>>' as implication        
                \t- '|' as disjunction        
                \t- '&' as conjunction        
                \t- '~' as negation
                Axioms must be valid logical formulas, and it accepts fully and correctly closed parentheses formulas!
                Some examples:
                (A >> B)\t\t\t<=>\t\t(A ⊃ B)
                (A | B)\t\t\t\t<=>\t\t(A ∨ B)
                (A & B)\t\t\t<=>\t\t(A ∧ B)
                ~A\t\t\t\t<=>\t\t¬A
                (A >> (~B | (C & D)))\t\t<=>\t\t(A ⊃ (¬B ∨ (C ∧ D)))
                You can also use the added axioms, with the ADDED AXIOM button. You can call for a hint, it shows a
                possible rule usage. And you can delete lines back, if you want to.
                Save button stands for saving the current deduction.
                """

        self.__help_label = QtWidgets.QLabel(help_text)
        self.__help_label.setFont(QFont("MS Shell Dlg 2", 12))

        self.__close_button = QtWidgets.QPushButton('Close')
        self.__close_button.clicked.connect(self.close)

        self.__layout.addWidget(self.__help_label)
        self.__layout.addWidget(self.__close_button)

        self.setLayout(self.__layout)
