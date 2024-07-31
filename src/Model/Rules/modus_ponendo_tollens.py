from Model.Rules.rule import Rule


class ModusPonendoTollens(Rule):
    """
    This class represents the Modus Ponendo Tollens detaching rule.
    It needs 2 formulas, and the first one must be a disjunction formula.
    The rule:
    {¬A ⊃ ¬B, B} |- A
    """
    def rule(self, implication_formula: str, formula_to_be_detached: str) -> (bool, str):
        """
        This function executes the Modus Ponendo Tollens, {¬A ⊃ ¬B, B} |- A rule.

        Args:
            implication_formula: the logical formula, that will be reduced with the formula_to_be_detached
            formula_to_be_detached: the formula that will be detached
        Returns:
            Tuple of (success_flag, result_formula).
            success_flag is a boolean indicating whether the modus ponendo tollens was successful.
            result_formula is the resulting formula after applying modus ponendo tollens,
            or an empty string if unsuccessful.
        """
        if not self._input_checker(implication_formula, formula_to_be_detached):
            return False, ''
        if not self._is_implication(implication_formula):
            return False, ''

        implication_formula = implication_formula.strip()
        implication_formula = implication_formula.replace(' ', '')
        implication_formula = implication_formula[1:-1]
        reversed_implication_formula = implication_formula[::-1]

        formula_to_be_detached = formula_to_be_detached.strip()
        formula_to_be_detached = formula_to_be_detached.replace(' ', '')
        reversed_formula_to_be_detached = formula_to_be_detached[::-1]

        modus_ponendo_tollensed_formula = ''
        for i in range(0, len(reversed_formula_to_be_detached)):
            if reversed_formula_to_be_detached[i] == reversed_implication_formula[i]:
                modus_ponendo_tollensed_formula += reversed_implication_formula[i]
            else:
                return False, ''

        implication_position = reversed_implication_formula.find(modus_ponendo_tollensed_formula)
        return_formula = reversed_implication_formula[implication_position + len(reversed_formula_to_be_detached):]
        if return_formula[0] == '~' and return_formula[1] == '>' and return_formula[2] == '>':
            return_formula = return_formula[3:]
            return_formula = return_formula[::-1]
            if return_formula[0] == '~':
                return True, return_formula[1:]
            else:
                return False, ''
        else:
            return False, ''
