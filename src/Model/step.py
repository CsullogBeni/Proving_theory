from Model.actions import Actions
from Model.Utils.utils import Utils


class Step:
    """
    Step class represents a step in proof theory.

    Attributes:
        step_id: (int) position, id of the step
        formula: (str) logical formula
        action: (Actions) step action (HIP, AXIOM, MP, MT, MTP, MPT, CS)
        axiom_details: (str) contains the substitutions of an axiom
        rule_implication: (int) if the action is MP, this is the index of the parent implication formula
        rule_detached: (int) if the action is MP, this is the index of the parent detached formula
    """

    def __init__(self,
                 step_id: int,
                 formula: str,
                 action: Actions,
                 axiom_details: str = '',
                 rule_implication: int = 0,
                 rule_detached: int = 0) -> None:
        """
        Constructor for Step. Requiters a valid logical formula

        Args:
            step_id: position, id of the step
            formula: logical formula
            action: step action (HIP, AXIOM, MP, MT, MTP, MPT, CS)
            axiom_details: if the Action is axiom, this will contain the substitution details
            rule_implication: if the action is a syntax rule, this is the index of the parent implication formula
            rule_detached: if the action is a syntax rule, this is the index of the parent detached formula
        """
        utils = Utils()
        if not utils.is_valid_formula(formula):
            raise ValueError
        if not utils.check_brackets(formula):
            raise ValueError
        if not isinstance(step_id, int) or step_id < 0:
            raise ValueError
        if not isinstance(action, Actions):
            raise ValueError
        if not isinstance(rule_implication, int):
            raise ValueError
        if not isinstance(rule_detached, int):
            raise ValueError

        formula = Utils.formula_re_formatter(formula)

        self.step_id = step_id
        self.formula = formula
        self.action = action
        self.axiom_details = axiom_details

        if (self.action != Actions.MP and self.action != Actions.MT and self.action != Actions.MTP and
                self.action != Actions.MPT and self.action != Actions.CS):
            if rule_implication != 0:
                raise ValueError
            if rule_detached != 0:
                raise ValueError
        else:
            self.rule_implication = rule_implication
            self.rule_detached = rule_detached
