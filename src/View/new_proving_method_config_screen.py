import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

from View.proving_method_screen import ProvingMethodScreen
from View.welcome_screen import WelcomeScreen
from View.help_dialog import HelpDialog

from Model.task_is_not_provable_exception import TaskIsNotProvableException


class NewProvingMethodConfigScreen(QDialog):
    """
    NewProvingMethodConfigScreen handles the configuration of a new proving method, handles user inputs.
    Checks if the inputs are correct. Such as all the formulas are valid logical formulas, brackets in formulas are
    placed correctly. Don't let the user go through if the inputs are incorrect. Gives help, how to give inputs.

    Attributes:
        __widget: Widget, that handles shown dialogs
    """

    def __init__(self, widget: QWidget) -> None:
        """
        Initialize the NewProvingMethodConfigScreen window. Loads the window_xmls\\new_proving_method_config_screen.ui
        xml
        """
        super(NewProvingMethodConfigScreen, self).__init__()
        loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'window_xmls\\new_proving_method_config_screen.ui'), self)
        self.__widget = widget

        self.continue_button.clicked.connect(self.__go_to_proving_method)
        self.back_button.clicked.connect(self.__go_to_welcome)
        self.help_button.clicked.connect(self.__get_help)

    def __go_to_proving_method(self) -> None:
        """
        Initializes a ProvingMethodScreen and gives the focus the that new screen.
        Checks the user inputs in the formula_set_text_edit and the consequence_formula_text_edit.
        All the formulas have to be valid formulas, and brackets must be correct. After checking the function use the
        Persistence.utils.saving_new_proving_config function and saves all data for the next go_to_proving_method
        window. If something is wrong the input, the function raises a message box.
        """
        formula_set = self.formula_set_text_edit.toPlainText().strip()
        consequence_formula = self.consequence_formula_text_edit.toPlainText().strip()
        if formula_set == "":
            formula_set = []
        if consequence_formula == "":
            self.__raise_message_box("You must give a consequence formula!")
            return
        from Model.Utils.utils import Utils
        if not self.__check_inputs(formula_set, consequence_formula):
            return
        if Utils.saving_new_proving_method_config(formula_set, consequence_formula):
            try:
                proving_method_screen = ProvingMethodScreen(self.__widget)
                proving_method_screen.init_model_with_new_config()
                self.__widget.addWidget(proving_method_screen)
                self.__widget.setCurrentIndex(self.__widget.currentIndex() + 1)
            except OSError:
                self.__raise_message_box("Something went wrong during initialize!")
            except ValueError:
                self.__raise_message_box("Something went wrong with the given formulas!")
            except TaskIsNotProvableException:
                pass
        else:
            self.__raise_message_box("Something is wrong with the formulas!")

    def __go_to_welcome(self) -> None:
        """
        Initializes a WelcomeScreen and gives the focus the that new screen.
        """
        welcome_screen = WelcomeScreen(self.__widget)
        self.__widget.addWidget(welcome_screen)
        self.__widget.setCurrentIndex(self.__widget.currentIndex() + 1)

    @staticmethod
    def __raise_message_box(text: str) -> None:
        """
        Raises a message box for the user, with the given input.

        Args:
             text (str): given input, that will be shown on the message box
        """
        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('Warning!')
        message_box.setText(text)
        message_box.exec_()

    @staticmethod
    def __get_help() -> None:
        """
        Initialize a HelpDialog for the user, and gives the focus to the new Dialog.
        """
        help_dialog = HelpDialog()
        help_dialog.exec_()

    def __check_inputs(self, formula_set: str, consequence_formula: str) -> bool:
        """
        Splits the formula set into formulas. Checks that each formula from the formula set, and the consequence formula
        are valid logical formulas, or not.

        Args:
            formula_set: contains the formulas of the formula set, separated by comas
            consequence_formula: the consequence formula

        Returns:
            True if all formulas are valid logical formulas, and brackets are correct in the formulas.
            False otherwise.
        """
        if not isinstance(consequence_formula, str):
            self.__raise_message_box('Incorrect consequence formula')
            return False

        if not self.__check_illegal_characters(consequence_formula):
            return False

        if not formula_set == []:
            formula_set = formula_set.replace(' ', '')
            formula_set = formula_set.replace('\t', '')
            formula_set = formula_set.replace('\n', '')

        if not self.__check_illegal_characters(formula_set):
            return False

        if ',' in formula_set:
            formula_set = formula_set.split(',')
            for formula in formula_set:
                if not formula:
                    continue
                if not self.__check_formula(formula):
                    return False
        else:
            if not self.__check_illegal_characters(formula_set):
                return False
            if not formula_set:
                return True
            if not self.__check_formula(formula_set):
                return False
        consequence_formula_to_be_checked = consequence_formula.replace(' ', '')
        consequence_formula_to_be_checked = consequence_formula_to_be_checked.replace('\t', '')
        consequence_formula_to_be_checked = consequence_formula_to_be_checked.replace('\n', '')
        if not self.__check_formula(consequence_formula_to_be_checked):
            return False
        return True

    def __check_illegal_characters(self, text: str) -> bool:
        """
        Checks if there is any character that should not be in a logical formula.
        Raise a messagebox if there is an illegal character
        Args:
            text: the  that contains the formula
        Returns:
            True if there is no illegal character.
            False otherwise.
        """
        for char in text:
            if char not in set('ABCDFGHJKLMWRTZU ()>|&~,'):
                self.__raise_message_box('Illegal character:\n' + char)
                return False
        return True

    def __check_formula(self, formula: str) -> bool:
        """
        Checks that the given formula is valid logical formula or not. And has complete brackets.
        Raise a messagebox if the formula is not valid, ot brackets are not correct.

        Args:
            formula: the original logical formula

        Returns:
            True if the formula is valid, and brackets are correct.
            False otherwise.
        """
        from Model.Utils.utils import Utils
        if (not isinstance(formula, str)) or (not Utils.is_valid_formula(formula)):
            self.__raise_message_box(
                'Invalid logical formula:\n' + formula)
            return False
        if not Utils.check_brackets(formula):
            self.__raise_message_box(
                'Incomplete or incorrect brackets:\n' + formula)
            return False
        return True
