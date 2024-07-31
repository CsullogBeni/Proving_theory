from Model.Rules.rule import Rule


class ModusTollendoPonens(Rule):
    """
    This class represents the Modus Tollendo Ponens detaching rule.
    It needs 2 formulas, and the first one must be a disjunction formula.
    The rule:
    {A ∨ B, ¬A} |- B

    Methods:
        rule: execute Modus Tollendo Ponens rule if it's feasible
    """
    def rule(self, disjunction_formula: str, formula_to_be_detached: str) -> (bool, str):
        """
        This function executes the Modus Tollendo Ponens, {A ∨ B, ¬A} |- B rule.

        Args:
            disjunction_formula: the logical formula, that will be reduced with the formula_to_be_detached
            formula_to_be_detached: the formula that will be detached
        Returns:
            Tuple of (success_flag, result_formula).
            success_flag is a boolean indicating whether the modus tollendo ponens was successful.
            result_formula is the resulting formula after applying modus tollendo ponens, or an empty string if
             unsuccessful.
        """
        if not self._input_checker(disjunction_formula, formula_to_be_detached):
            return False, ''
        if not self._contains_disjunction(disjunction_formula):
            return False, ''
        if not Rule.is_negation(formula_to_be_detached):
            return False, ''

        disjunction_formula = disjunction_formula.strip()
        disjunction_formula = disjunction_formula.replace(' ', '')
        disjunction_formula = disjunction_formula[1:-1]

        formula_to_be_detached = formula_to_be_detached.strip()
        formula_to_be_detached = formula_to_be_detached.replace(' ', '')
        formula_to_be_detached = formula_to_be_detached[1:]

        modus_ponendo_tollensed_formula = ''
        for i in range(0, len(formula_to_be_detached)):
            if formula_to_be_detached[i] == disjunction_formula[i]:
                modus_ponendo_tollensed_formula += disjunction_formula[i]
            else:
                return False, ''

        implication_position = disjunction_formula.find(modus_ponendo_tollensed_formula)
        return_formula = disjunction_formula[implication_position + len(formula_to_be_detached):]
        if return_formula[0] == '|':
            return_formula = return_formula[1:]
            return True, return_formula
        else:
            return False, ''
