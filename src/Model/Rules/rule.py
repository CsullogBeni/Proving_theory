from abc import ABC, abstractmethod

from Model.Utils.utils import Utils


class Rule(ABC):
    """
    Abstract class contains abstract method rule. Contains other functions for syntax rules, that inherited from this
    class.

    """

    @staticmethod
    def _is_implication(formula_string: str) -> bool:
        """
        Decides whether a formula is an implication formula, or not. If a formula contains '>>', it's
        an implication formula, due to precedence.

        Args:
            formula_string: logical formula
        Returns:
             If the formula is implication formula, return True, otherwise False.
        """
        if not isinstance(formula_string, str):
            return False
        if not Utils.is_valid_formula(formula_string):
            return False
        if not Utils.check_brackets(formula_string):
            return False
        return '>>' in formula_string

    @staticmethod
    def is_negation(formula_string: str) -> bool:
        """
        Decides whether a formula is a negation formula, or not. If the formulas first character is '~', then it's
        negated

        Args:
            formula_string: logical formula
        Returns:
             If the formula is negation formula, return True, otherwise False.
        """
        if not isinstance(formula_string, str):
            return False
        if not Utils.is_valid_formula(formula_string):
            return False
        if not Utils.check_brackets(formula_string):
            return False
        if not formula_string:
            return False
        return '~' == formula_string[0]

    @staticmethod
    def _contains_disjunction(formula_string: str) -> bool:
        """
        Decides whether a formula contains a disjunction, or not.

        Args:
            formula_string: logical formula
        Returns:
            If the formula contains a disjunction, return True, otherwise False.
        """
        if not isinstance(formula_string, str):
            return False
        if not Utils.is_valid_formula(formula_string):
            return False
        if not Utils.check_brackets(formula_string):
            return False
        if not formula_string:
            return False
        return '|' in formula_string

    @staticmethod
    def _input_checker(implication_formula: str,
                       formula_to_be_detached: str,
                       conditional_syllogism: bool = False) -> bool:
        """
        Checks that the inputs are strings, valid logical formulas, and all brackets are correct

        Args:
            implication_formula:  implication logical formula (mut contain implication operation)
            formula_to_be_detached: logical formula, that will be detached

        :return:
            True if the inputs meet the above assumptions
            False otherwise
        """
        if not isinstance(implication_formula, str):
            return False
        if not isinstance(formula_to_be_detached, str):
            return False
        if not implication_formula:
            return False
        if not formula_to_be_detached:
            return False
        if not Utils.is_valid_formula(implication_formula):
            return False
        if not Utils.is_valid_formula(formula_to_be_detached):
            return False
        if not Utils.check_brackets(implication_formula):
            return False
        if not Utils.check_brackets(formula_to_be_detached):
            return False
        if not conditional_syllogism:
            if len(implication_formula) <= len(formula_to_be_detached):
                return False
        return True

    @staticmethod
    @abstractmethod
    def rule(implication_formula: str, formula_to_be_detached: str) -> (bool, str):
        """
        Function that will be overwritten, in the children classes. The function will contain the syntax rules from
        proving theory:
            -Modus Ponens
            -Modus tollens
            -Modus Tollendo Ponens
            -Modus Ponendo Tollens
            -Conditional Syllogism
        One of them will be the current rule, when over writing this function.

        Args:
            implication_formula: logical formula, must be an implication formula
            formula_to_be_detached: logical formula, that will be detached from the implication formula

        Returns:
            Tuple of (success_flag, result_formula).
            success_flag is a boolean indicating whether the current rule using was successful.
            result_formula is the resulting formula after applying the current rule, or an empty string if unsuccessful.
        """
        return False, ''
