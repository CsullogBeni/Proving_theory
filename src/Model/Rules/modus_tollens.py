from Model.Rules.rule import Rule


class ModusTollens(Rule):
    """
    This class represents the Modus Tollens detaching rule.
    It needs 2 formulas, and the first one must be an implication formula.
    The rule:
    {A ⊃ B, ¬B} |- ¬A
    """
    def rule(self, implication_formula: str, formula_to_be_detached: str) -> (bool, str):
        """
        This function executes the Modus Tollens, {A ⊃ B, ¬B} |- ¬A rule.

        Args:
            implication_formula: the logical formula, that will be reduced with the formula_to_be_detached
            formula_to_be_detached: the formula that will be detached
        Returns:
            Tuple of (success_flag, result_formula).
            success_flag is a boolean indicating whether the modus tollens was successful.
            result_formula is the resulting formula after applying modus ponens, or an empty string if unsuccessful.
        """
        if not self._input_checker(implication_formula, formula_to_be_detached):
            return False, ''
        if not self.is_negation(formula_to_be_detached):
            return False, ''
        if not self._is_implication(implication_formula):
            return False, ''

        implication_formula = implication_formula.strip()
        implication_formula = implication_formula.replace(' ', '')
        implication_formula = implication_formula[1:-1]
        reversed_implication_formula = implication_formula[::-1]

        formula_to_be_detached = formula_to_be_detached.strip()
        formula_to_be_detached = formula_to_be_detached.replace(' ', '')
        formula_to_be_detached = formula_to_be_detached[1:]
        reversed_formula_to_be_detached = formula_to_be_detached[::-1]

        modus_tollens_formula = ''
        for i in range(0, len(reversed_formula_to_be_detached)):
            if reversed_implication_formula[i] == reversed_formula_to_be_detached[i]:
                modus_tollens_formula += reversed_implication_formula[i]
            else:
                return False, ''

        implication_position = reversed_implication_formula.find(modus_tollens_formula)
        return_formula = reversed_implication_formula[implication_position + len(reversed_formula_to_be_detached):]
        if return_formula[0] == '>' and return_formula[1] == '>':
            return_formula = return_formula[2:]
            return True, '~' + (return_formula[::-1])
        else:
            return False, ''
