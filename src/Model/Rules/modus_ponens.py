from Model.Rules.rule import Rule


class ModusPonens(Rule):
    """
    This class represents the Modus Ponens detaching rule.
    It needs 2 formulas, and the first one must be an implication formula.
    The rule:
    {A ⊃ B, A} |- B
    """
    def rule(self, implication_formula: str, formula_to_be_detached: str) -> (bool, str):
        """
        This function executes the Modus Ponens, {A ⊃ B, A} |- B rule.

        Args:
            implication_formula: the logical formula, that will be reduced with the formula_to_be_detached
            formula_to_be_detached: the formula that will be detached
        Returns:
            Tuple of (success_flag, result_formula).
            success_flag is a boolean indicating whether the modus ponens was successful.
            result_formula is the resulting formula after applying modus ponens, or an empty string if unsuccessful.
        """
        if not self._input_checker(implication_formula, formula_to_be_detached):
            return False, ''
        if not self._is_implication(implication_formula):
            return False, ''

        implication_formula = implication_formula.strip()
        implication_formula = implication_formula.replace(' ', '')
        implication_formula = implication_formula[1:-1]

        formula_to_be_detached = formula_to_be_detached.strip()
        formula_to_be_detached = formula_to_be_detached.replace(' ', '')

        modus_ponensed_formula = ''
        for i in range(0, len(formula_to_be_detached)):
            if formula_to_be_detached[i] == implication_formula[i]:
                modus_ponensed_formula += implication_formula[i]
            else:
                return False, ''

        implication_position = implication_formula.find(modus_ponensed_formula)
        return_formula = implication_formula[implication_position + len(formula_to_be_detached):]
        if return_formula[0] == '>' and return_formula[1] == '>':
            return_formula = return_formula[2:]
            return True, return_formula
        else:
            return False, ''
