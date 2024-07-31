from Model.model import Model
from Model.Rules.rule import Rule
from Model.actions import Actions
from Model.Utils.utils import Utils
from Model.step import Step
from Model.formula_in_steps_exception import FormulaInStepsException


class Solver:
    """
    The clas represents a possible was to solve tasks. Tries to solve the given Model object's task.
    """
    @staticmethod
    def solve(model_param: Model) -> tuple:
        """
        Tries to solve a Model object's task (consequence).
        Try to use all hyp, then use continuously the syntax rules and substitute different formulas into all axioms.
        If the task is solved, then the function calls the get_proving_theory recursive function that filters the
        actually important steps. This will be returned.

        model_param: Model, that contains the task

        Returns:
            A tuple, that contains a true and the important steps if solving was successful.
            Otherwise, the tuple will contain a false value and an empty list.
        """
        model = model_param

        if not isinstance(model, Model):
            return False, []

        if not model.task_is_provable():
            return False, []

        if model.consequence_formula == '':
            return False, []

        if not model.steps:
            model.steps = []

        if model.formula_set_contains_tautology():
            model.delete_tautologies()

        variables = []
        for formula in model.formula_set:
            model.add_step(formula, Actions.HYP)
            variables.append(formula)
            variables.append('~' + formula)
            vars_in_formula = Utils.get_formula_variables(formula)
            for var in vars_in_formula:
                variables.append(var)
                variables.append('~' + var)
            if Rule.is_negation(formula):
                if Utils.is_valid_formula(formula[1:]):
                    variables.append(formula[1:])
        variables.append(model.consequence_formula)
        variables.append('~' + model.consequence_formula)

        variables = sorted(list(set(variables)))

        if not Solver.use_syntax_rules(model):
            return False, ''

        if not Solver.use_axioms(model, variables):
            return False, ''

        if not Solver.use_syntax_rules(model):
            return False, ''

        indexes = sorted(
            list(set(Solver.get_proving_theory(model, model.steps[len(model.steps) - 1]) + [len(model.steps) - 1])))
        steps_strings = model.get_steps_string()
        filtered_steps = []

        for idx in indexes:
            filtered_steps.append(steps_strings[idx])

        if model.end:
            return True, filtered_steps
        else:
            return False, ''

    @staticmethod
    def get_proving_theory(model: Model, step: Step) -> list:
        """
        Recursive function that filters the important steps from the steps list.

        Args:
            model: The model that contains the steps list
            step: the actual step, of which parents are searched

        Returns:
            A list that contains the indexes of the important steps
        """
        if not isinstance(model, Model):
            return []
        if not isinstance(step, Step):
            return []
        if step.action == Actions.AXIOM:
            return [step.step_id]
        elif step.action == Actions.HYP:
            return [step.step_id]
        else:
            first_param = model.steps[step.step_id].rule_implication
            second_param = model.steps[step.step_id].rule_detached
            return ([step.step_id] + Solver.get_proving_theory(model, model.steps[first_param]) +
                    Solver.get_proving_theory(model, model.steps[second_param]))

    @staticmethod
    def use_syntax_rules(model: Model) -> bool:
        """
        Tries to use all syntax rule to all steps in step list form the model

        Args:
            model: Contains the steps, and the models.add_steps is used

        Returns:
            True if the syntax rule usages were successful.
            False otherwise.
        """
        if not isinstance(model, Model):
            return False
        for rule_1, _ in enumerate(model.steps):
            for rule_2, _ in enumerate(model.steps):
                try:
                    model.add_step('', Actions.MP, implication_formula_number=rule_1, formula_to_be_detached_number=rule_2)
                    if model.end:
                        break
                    model.add_step('', Actions.MT, implication_formula_number=rule_1, formula_to_be_detached_number=rule_2)
                    if model.end:
                        break
                    model.add_step('', Actions.MTP, implication_formula_number=rule_1, formula_to_be_detached_number=rule_2)
                    if model.end:
                        break
                    model.add_step('', Actions.MPT, implication_formula_number=rule_1, formula_to_be_detached_number=rule_2)
                    if model.end:
                        break
                    model.add_step('', Actions.CS, implication_formula_number=rule_1, formula_to_be_detached_number=rule_2)
                    if model.end:
                        break
                except FormulaInStepsException:
                    continue
            if model.end:
                break
        return True

    @staticmethod
    def use_axioms(model: Model, variables: list) -> bool:
        """
        Tries to substitute variables into the axioms.

        Args:
            model: Contains the steps, and the models.add_steps is used.
            variables: thees variables are substituted into the axioms.

        Returns:
            True if the substitutions were successful.
            False otherwise.
        """
        for axiom in model.base_axioms:
            number_of_vars = len(Utils.get_formula_variables(axiom))

            if number_of_vars == 1:
                for var in variables:
                    try:
                        model.add_step(axiom, Actions.AXIOM, data=[var])
                    except FormulaInStepsException:
                        pass

            if number_of_vars == 2:
                for var_1 in variables:
                    for var_2 in variables:
                        try:
                            model.add_step(axiom, Actions.AXIOM, data=[var_1, var_2])
                            model.add_step(axiom, Actions.AXIOM, data=[var_2, var_1])
                            model.add_step(axiom, Actions.AXIOM, data=[var_1, var_1])
                            model.add_step(axiom, Actions.AXIOM, data=[var_2, var_2])
                        except FormulaInStepsException:
                            pass

            if number_of_vars == 3:
                for var_1 in variables:
                    for var_2 in variables:
                        for var_3 in variables:
                            try:
                                model.add_step(axiom, Actions.AXIOM, data=[var_1, var_2, var_3])
                                model.add_step(axiom, Actions.AXIOM, data=[var_1, var_3, var_2])
                                model.add_step(axiom, Actions.AXIOM, data=[var_2, var_1, var_3])
                                model.add_step(axiom, Actions.AXIOM, data=[var_2, var_3, var_1])
                                model.add_step(axiom, Actions.AXIOM, data=[var_3, var_1, var_2])
                                model.add_step(axiom, Actions.AXIOM, data=[var_3, var_2, var_1])

                                model.add_step(axiom, Actions.AXIOM, data=[var_1, var_1, var_1])
                                model.add_step(axiom, Actions.AXIOM, data=[var_2, var_2, var_2])
                                model.add_step(axiom, Actions.AXIOM, data=[var_3, var_3, var_3])

                                model.add_step(axiom, Actions.AXIOM, data=[var_1, var_1, var_2])
                                model.add_step(axiom, Actions.AXIOM, data=[var_1, var_1, var_3])
                                model.add_step(axiom, Actions.AXIOM, data=[var_1, var_2, var_1])
                                model.add_step(axiom, Actions.AXIOM, data=[var_1, var_3, var_1])
                                model.add_step(axiom, Actions.AXIOM, data=[var_2, var_1, var_1])
                                model.add_step(axiom, Actions.AXIOM, data=[var_3, var_1, var_1])

                                model.add_step(axiom, Actions.AXIOM, data=[var_2, var_2, var_1])
                                model.add_step(axiom, Actions.AXIOM, data=[var_2, var_2, var_3])
                                model.add_step(axiom, Actions.AXIOM, data=[var_2, var_1, var_2])
                                model.add_step(axiom, Actions.AXIOM, data=[var_2, var_3, var_2])
                                model.add_step(axiom, Actions.AXIOM, data=[var_1, var_2, var_2])
                                model.add_step(axiom, Actions.AXIOM, data=[var_3, var_2, var_2])

                                model.add_step(axiom, Actions.AXIOM, data=[var_3, var_3, var_1])
                                model.add_step(axiom, Actions.AXIOM, data=[var_3, var_3, var_2])
                                model.add_step(axiom, Actions.AXIOM, data=[var_3, var_1, var_3])
                                model.add_step(axiom, Actions.AXIOM, data=[var_3, var_2, var_3])
                                model.add_step(axiom, Actions.AXIOM, data=[var_1, var_3, var_3])
                                model.add_step(axiom, Actions.AXIOM, data=[var_2, var_3, var_3])
                            except FormulaInStepsException:
                                pass
        return True
