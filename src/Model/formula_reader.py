import sympy.logic.boolalg
from sympy import *
from Model.Utils.utils import Utils


class FormulaReader:
    """
    This class can convert strings to logical formulas, generate truth table to the formulas and can decide
    that formulas are tautologies or not.

    Attributes:
        __formula_string: (str) raw formula itself
        __formula: (logical_formula) parsed logical formula
        __variable_list: (str list) the formula's variable
        __truth_table: (truth table) contains formula's all variable, and all interpretations with substitution value
    """
    def __init__(self) -> None:
        """
        Constructor for FormulaReader
        """
        self.__formula_string = ''
        self.__formula = None
        self.__variable_list = []
        self.__truth_table = None

    def __formula_converter(self, current_formula_string: str) -> None:
        """
        Converts strings to logical formula.

        Gets all variables from the logical formula into formula_variables.
        sympy.parse_expr(self.formula_string) parse a string into a logical formula
        """
        if not Utils.is_valid_formula(current_formula_string):
            return
        self.__formula_string = current_formula_string
        formula_variables = set(symbols([c for c in self.__formula_string if c.isalpha()]))
        self.__variable_list = list(formula_variables)
        self.__formula = sympy.parse_expr(self.__formula_string)

    def __create_truth_table(self) -> None:
        """
        Create a truth table from the formula with sympy.logic.boolalg.truth_table() method
        The truth table contain all values for the variation of the formula.
        """
        if not Utils.is_valid_formula(self.__formula_string):
            return
        self.__truth_table = sympy.logic.boolalg.truth_table(self.__formula_string, self.__variable_list)

    def is_tautology(self, current_formula_string: str) -> bool:
        """
        This function returns whether a formula is tautology or not, by checking a formula's truth table, if there is a
        false interpretation, than the formula, is not tautology

        Args:
            current_formula_string: this formula will be converted into a logical formula, and a truth table is
            generated for this formula
        Returns:
            whether a formula is tautology or not
        """
        if current_formula_string == '':
            return False
        if not Utils.is_valid_formula(current_formula_string):
            return False
        self.__formula_converter(current_formula_string)
        self.__create_truth_table()
        for row in self.__truth_table:
            if not row[len(row)-1]:
                return False
        return True
