import string

from Model.Rules.rule import Rule
from Model.Utils.utils import Utils


class ConditionalSyllogism(Rule):
    """
    This class represents the Conditional Syllogism detaching rule.
    It needs 2 formulas, and both of them must be an implication formula.
    The rule:
    {A ⊃ B, B ⊃ C} |- A ⊃ C
    """
    def rule(self, first_implication_formula: str, second_implication_formula: str) -> (bool, str):
        """
        This function executes the Modus Tollendo Ponens, {A ⊃ B, B ⊃ C} |- A ⊃ C rule.

        Args:
            first_implication_formula: the first implication formula, that contains the second implication first
             part formula
            second_implication_formula: the second implication formula
        Returns:
            Tuple of (success_flag, result_formula).
            success_flag is a boolean indicating whether the modus tollendo ponens was successful.
            result_formula is the resulting formula after applying modus tollendo ponens, or an empty string if
             unsuccessful.
        """
        if not self._input_checker(first_implication_formula, second_implication_formula,
                                         conditional_syllogism=True):
            return False, ''
        if not self._is_implication(first_implication_formula):
            return False, ''
        if not self._is_implication(second_implication_formula):
            return False, ''

        first_implication_formula = first_implication_formula.strip()
        first_implication_formula = first_implication_formula.replace(' ', '')
        first_implication_formula = first_implication_formula[1:-1]

        second_implication_formula = second_implication_formula.strip()
        second_implication_formula = second_implication_formula.replace(' ', '')
        second_implication_formula = second_implication_formula[1:-1]

        conditional_syllogism_formula = ''
        for idx in range(0, len(first_implication_formula)):
            idx_error = False
            for jdx in range(0, len(second_implication_formula)):
                try:
                    if first_implication_formula[idx + jdx] == second_implication_formula[jdx]:
                        conditional_syllogism_formula += second_implication_formula[jdx]
                        if idx == len(first_implication_formula) - 1:
                            break
                    else:
                        conditional_syllogism_formula = ''
                        break
                except IndexError:
                    idx_error = True
                    break
            if idx_error:
                break
            if idx == len(first_implication_formula)-1:
                break

        if not Utils.is_valid_formula(conditional_syllogism_formula):
            return False, ''
        if not Utils.check_brackets(conditional_syllogism_formula):
            return False, ''

        last_index = first_implication_formula.rfind(conditional_syllogism_formula)
        if last_index == -1:
            return False, ''
        else:
            return_formula = first_implication_formula[:last_index]

        first_index = second_implication_formula.find(conditional_syllogism_formula)
        if first_index == -1:
            return False, ''
        second_implication_formula = second_implication_formula[len(conditional_syllogism_formula) + 2:]

        return_formula = '(' + return_formula + second_implication_formula + ')'

        if not Utils.is_valid_formula(return_formula):
            return False, ''
        if not Utils.check_brackets(return_formula):
            return False, ''

        return True, return_formula
