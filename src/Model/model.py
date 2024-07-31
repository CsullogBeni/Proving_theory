from Model.step import Step
from Model.actions import Actions
from Model.Utils.utils import Utils
from Persistence.axiom_reader import AxiomReader
from Persistence.data_access import DataAccess
from Model.formula_reader import FormulaReader
from Model.Rules.modus_ponens import ModusPonens
from Model.Rules.modus_tollens import ModusTollens
from Model.Rules.modus_tollendo_ponens import ModusTollendoPonens
from Model.Rules.modus_ponendo_tollens import ModusPonendoTollens
from Model.Rules.conditional_syllogism import ConditionalSyllogism
from Model.formula_in_steps_exception import FormulaInStepsException


class Model:
    """
    This class handles the business logic. This class tries to model Proving Theory.

    Attributes:
        formula_set: (str list) list of logical formulas, as string, hypothesis
        consequence_formula: (str) consequence logical formula, that will should be proved
        steps: (Step list) list of steps in the proving method
        number_of_steps: (int) current number of steps. Used as an id for new steps as well
        end: (bool) represents that the consequence_formula is proved, or not
        base_axioms: (str list) list that contains the base axioms (read from json file)
        added_axioms: (str list) list that contains added axioms (added in runtime)
        __axiom_reader: (AxiomReader) sets the base axioms for the model. Use the AxiomReader.read_axioms function
        __data_access: (DataAccess) manages files and database. Handles saving loading functions.
    """

    def __init__(self,
                 formula_set: list = None,
                 consequence_formula: str = None,
                 file_path: str = None) -> None:
        """
        Constructor to Model class.
        If the constructor gets the formula_set and consequence_formula as param, then the function
        creates the model object, init everything. But if it gets only the file_path as param, then it
        reads all the data form the given_file_path

        Raises:
            ValueError

        Args:
            formula_set: list of logical formulas, as string, hypothesis
            consequence_formula: consequence logical formula, that will should be proved
            file_path: string to  a file, that contains data for a model.
        """
        self.__axiom_reader = AxiomReader()
        self.__data_access = DataAccess()
        self.base_axioms = self.__axiom_reader.read_axioms_from_json()
        if not self.__axiom_checker(self.base_axioms):
            raise ValueError
        self.added_axioms = []

        self.formula_set = None
        self.consequence_formula = None
        self.steps = None
        self.number_of_steps = None
        self.end = None

        if (formula_set or (formula_set == [])) and consequence_formula and (file_path is None):
            try:
                self.__input_checker(formula_set, consequence_formula)
            except ValueError:
                raise ValueError

            self.formula_set = []
            for formula in formula_set:
                self.formula_set.append(Utils.formula_re_formatter(formula))

            self.consequence_formula = Utils.formula_re_formatter(consequence_formula)
            self.steps = []
            self.number_of_steps = 0
            self.end = False

        elif (formula_set is None) and (consequence_formula is None) and file_path:
            try:
                if not self.load_model(file_path):
                    raise ValueError
            except Exception:
                raise ValueError
        else:
            raise ValueError

        self.__check_end()

    def add_step(self,
                 formula: str,
                 action: Actions,
                 implication_formula_number: int = 0,
                 formula_to_be_detached_number: int = 0,
                 data: list = None) -> bool:
        """
        Tries to add the current_step to steps, if possible.
        Checks the action and tries to execute the correct action, after conflict resolution

        Args:
            formula: logical formula, related to the action-param
            action: that will be executed
            implication_formula_number: index of the rule functions first param, in steps
            formula_to_be_detached_number: index of the rule functions second param, in steps
            data: list of logical formula strings. List length must be exactly the same as how many
                variable are in the current step's formula.

        Returns:
            Whether the addition was successful or not
        """
        if data is None:
            data = []
        if self.end:
            return False
        if not isinstance(action, Actions):
            return False
        try:
            current_step = Step(self.number_of_steps, formula, action, rule_implication=implication_formula_number,
                                rule_detached=formula_to_be_detached_number)
        except ValueError:
            return False

        if current_step.action == Actions.HYP:
            current_step = self.__action_hyp(current_step)
        elif current_step.action == Actions.AXIOM:
            current_step = self.__action_axiom(current_step, data)
        elif current_step.action == Actions.MP:
            current_step = self.__action_syntax_rule(current_step, implication_formula_number,
                                                     formula_to_be_detached_number)
        elif current_step.action == Actions.MT:
            current_step = self.__action_syntax_rule(current_step, implication_formula_number,
                                                     formula_to_be_detached_number)
        elif current_step.action == Actions.MTP:
            current_step = self.__action_syntax_rule(current_step, implication_formula_number,
                                                     formula_to_be_detached_number)
        elif current_step.action == Actions.MPT:
            current_step = self.__action_syntax_rule(current_step, implication_formula_number,
                                                     formula_to_be_detached_number)
        elif current_step.action == Actions.CS:
            current_step = self.__action_syntax_rule(current_step, implication_formula_number,
                                                     formula_to_be_detached_number)

        else:
            current_step = None

        if current_step is None:
            return False

        try:
            if not self.__steps_append(current_step):
                return False
        except FormulaInStepsException:
            raise FormulaInStepsException
        self.number_of_steps += 1
        self.__check_end()
        return True

    @staticmethod
    def __input_checker(formula_set: list, consequence_formula: str) -> None:
        """
        Checks that the inputs are correct in the constructor. Checks all the formulas are valid, and correct.

        Args:
            formula_set: list of logical formulas, as string, hypothesis
            consequence_formula: consequence logical formula, that will should be proved

        Raises:
             ValueError: if one of the formulas are not valid
        """
        if not isinstance(consequence_formula, str):
            raise ValueError
        if consequence_formula == '':
            raise ValueError
        if not isinstance(formula_set, list):
            raise ValueError
        if len(formula_set) != 0 or formula_set != ['']:
            for formula in formula_set:
                if not isinstance(formula, str):
                    raise ValueError
                if formula == '':
                    raise ValueError
                if not Utils.is_valid_formula(formula):
                    raise ValueError
                if not Utils.check_brackets(formula):
                    raise ValueError
        if not Utils.is_valid_formula(consequence_formula):
            raise ValueError
        if not Utils.check_brackets(consequence_formula):
            raise ValueError

    @staticmethod
    def __axiom_checker(formula_list: list) -> bool:
        """
        Checks whether the formulas of the formula list are all axioms, always True

        Args:
            formula_list (str list): list of formulas
        Returns:
            True if the formula_set contains only axioms
            False otherwise
        """
        formula_reader = FormulaReader()
        for formula in formula_list:
            if not formula_reader.is_tautology(formula):
                return False
        return True

    def __action_hyp(self, step: Step) -> Step | None:
        """
        Checks whether hypothesis is executable.

        Args:
            step (Step): current step
        Returns:
            None if formula_step does not contain the current step's formula
            Otherwise return the current step
        """
        if self.end:
            return None
        if not isinstance(step, Step):
            return None
        if step.action != Actions.HYP:
            return None
        if step.formula == '':
            return None
        if step.formula not in self.formula_set:
            return None
        return step

    def __action_axiom(self,
                       step: Step,
                       data: list,
                       base_axiom: bool = True) -> Step | None:
        """
        Checks whether axiom is executable. Tries to replace the current step's formula's variables with
        logical formulas which contained by data

        Args:
            step: current step, step's formula needs to a be an axiom
            data: list of logical formula strings. List length must be exactly the same as how many
                variable are in the current step's formula.
            base_axiom: if true, then using the base axioms, otherwise using the added axioms.
        Returns:
            None if replacing throws ValueError
            Otherwise return the current step
        """
        if self.end:
            return None
        if step.action != Actions.AXIOM:
            return None
        if step.formula == '':
            return None
        if data is []:
            return None
        axiom_id = 0
        if base_axiom:
            if step.formula not in self.base_axioms:
                return None
            else:
                for count, formula in enumerate(self.base_axioms):
                    if formula == step.formula:
                        axiom_id = count + 1
                        break
        else:
            if step.formula not in self.added_axioms:
                return None
            else:
                for count, formula in enumerate(self.added_axioms):
                    if formula == step.formula:
                        axiom_id = count + 1 + (len(self.base_axioms))
                        break
        for formula in data:
            if formula == '':
                return None
            if not Utils.is_valid_formula(formula):
                return None
            if not Utils.check_brackets(formula):
                return None
        try:
            variables = Utils.get_formula_variables(step.formula)
            binded_list = Utils.bind_variables_to_substitution_data(variables, data)
            step.formula = Utils.formula_re_formatter(Utils.replace_in_formula(step.formula, binded_list))

            step.axiom_details = '[AXIOM: ' + str(axiom_id) + '.'
            for idx in range(len(variables)):
                step.axiom_details = step.axiom_details + ' ' + variables[idx] + '=' + Utils.formula_re_formatter(
                    data[idx])
            step.axiom_details = step.axiom_details + ']'
        except ValueError:
            return None
        return step

    def __action_syntax_rule(self,
                             step: Step,
                             implication_formula_number: int,
                             formula_to_be_detached_number: int) -> Step | None:
        """
        Tries to execute the given syntax rule with the input formulas, represented with indexes.

        Args:
            step: current step
            implication_formula_number: index of the implication formula, in steps
            formula_to_be_detached_number: index of the formula to be detached, in steps

        Returns:
            None if the syntax rule in use returns False
            Otherwise return the current step, current step's formula will be the return value of the syntax rule
            function
        """
        if self.end:
            return None
        if not isinstance(step, Step):
            return None
        if step.action == Actions.HYP or step.action == Actions.AXIOM:
            return None
        if not isinstance(implication_formula_number, int):
            return None
        if not isinstance(formula_to_be_detached_number, int):
            return None

        imp_idx = implication_formula_number
        det_idx = formula_to_be_detached_number
        if imp_idx == det_idx:
            return None
        if imp_idx < 0:
            return None
        if det_idx < 0:
            return None
        try:
            if self.steps[imp_idx] == '' or self.steps[det_idx] == '':
                return None
        except IndexError:
            return None

        try:
            if step.action == Actions.MP:
                current_syntax_rule = self.__action_modus_ponens(step, imp_idx, det_idx)
            elif step.action == Actions.MT:
                current_syntax_rule = self.__action_modus_tollens(step, imp_idx, det_idx)
            elif step.action == Actions.MPT:
                current_syntax_rule = self.__action_modus_ponendo_tollens(step, imp_idx, det_idx)
            elif step.action == Actions.MTP:
                current_syntax_rule = self.__action_modus_tollendo_tollens(step, imp_idx, det_idx)
            elif step.action == Actions.CS:
                current_syntax_rule = self.__action_conditional_syllogism(step, imp_idx, det_idx)
            else:
                return None
        except IndexError:
            return None

        if current_syntax_rule is None:
            return None
        return step

    def __action_modus_ponens(self,
                              step: Step,
                              implication_formula_number: int,
                              formula_to_be_detached_number: int) -> Step | None:
        """
        Tries to execute modus ponens rule, if possible.
        If it's possible, the  current step will contain the ModusPonens.rule() return value.

        Args:
            step: current step
            implication_formula_number: index of the implication formula, in steps
            formula_to_be_detached_number: index of the formula to be detached, in steps
        Returns:
            None if modus_ponens returns False
            Otherwise return the current step, current step's formula will be the return value of the MP function
        """
        try:
            current_mp = ModusPonens.rule(ModusPonens(), (self.steps[implication_formula_number]).formula,
                                          (self.steps[formula_to_be_detached_number]).formula)
        except IndexError:
            return None
        if not current_mp[0]:
            return None
        else:
            current_formula = current_mp[1]
            current_formula = Utils.formula_re_formatter(current_formula)
            step.formula = current_formula
        return step

    def __action_modus_tollens(self,
                               step: Step,
                               implication_formula_number: int,
                               formula_to_be_detached_number: int) -> Step | None:
        """
        Tries to execute modus tollens rule, if possible.
        If it's possible, the  current step will contain the ModusTollens.rule() return value.

        Args:
            step: current step
            implication_formula_number: index of the implication formula, in steps
            formula_to_be_detached_number: index of the formula to be detached, in steps
        Returns:
            None if modus tollens returns False
            Otherwise return the current step, current step's formula will be the return value of the MT function
        """
        try:
            current_mt = ModusTollens.rule(ModusTollens(), (self.steps[implication_formula_number]).formula,
                                           (self.steps[formula_to_be_detached_number]).formula)
        except IndexError:
            return None
        if not current_mt[0]:
            return None
        else:
            current_formula = current_mt[1]
            current_formula = Utils.formula_re_formatter(current_formula)
            step.formula = current_formula
        return step

    def __action_modus_tollendo_tollens(self,
                                        step: Step,
                                        disjunction_formula_number: int,
                                        formula_to_be_detached_number: int) -> Step | None:
        """
       Tries to execute modus tollendo ponens rule, if possible.
       If it's possible, the  current step will contain the ModusTollendoPonens.rule() return value.

       Args:
           step: current step
           disjunction_formula_number: index of the disjunction formula, in steps
           formula_to_be_detached_number: index of the formula to be detached, in steps
       Returns:
           None if modus tollendo ponens returns False
           Otherwise return the current step, current step's formula will be the return value of the MTP function
       """
        try:
            current_mtp = ModusTollendoPonens.rule(ModusTollendoPonens(),
                                                   (self.steps[disjunction_formula_number]).formula,
                                                   (self.steps[formula_to_be_detached_number]).formula)
        except IndexError:
            return None
        if not current_mtp[0]:
            return None
        else:
            current_formula = current_mtp[1]
            current_formula = Utils.formula_re_formatter(current_formula)
            step.formula = current_formula
        return step

    def __action_modus_ponendo_tollens(self,
                                       step: Step,
                                       disjunction_formula_number: int,
                                       formula_to_be_detached_number: int) -> Step | None:
        """
       Tries to execute modus ponendo tollens rule, if possible.
       If it's possible, the  current step will contain the ModusPonendoTollens.rule() return value.

       Args:
           step: current step
           disjunction_formula_number: index of the disjunction formula, in steps
           formula_to_be_detached_number: index of the formula to be detached, in steps
       Returns:
           None if modus ponendo tollens returns False
           Otherwise return the current step, current step's formula will be the return value of the MPT function
       """
        try:
            current_mpt = ModusPonendoTollens.rule(ModusPonendoTollens(),
                                                   (self.steps[disjunction_formula_number]).formula,
                                                   (self.steps[formula_to_be_detached_number]).formula)
        except IndexError:
            return None
        if not current_mpt[0]:
            return None
        else:
            current_formula = current_mpt[1]
            current_formula = Utils.formula_re_formatter(current_formula)
            step.formula = current_formula
        return step

    def __action_conditional_syllogism(self,
                                       step: Step,
                                       first_implication_formula_number: int,
                                       second_implication_formula_number: int) -> Step | None:
        """
       Tries to execute conditional syllogism rule, if possible.
       If it's possible, the  current step will contain the ConditionalSyllogism.rule() return value.

       Args:
           step: current step
           first_implication_formula_number: index of the first implication formula, in steps
           second_implication_formula_number: index of the second implication formula, in steps
       Returns:
           None if conditional syllogism returns False
           Otherwise return the current step, current step's formula will be the return value of the CS function
       """
        try:
            current_cs = ConditionalSyllogism.rule(ConditionalSyllogism(),
                                                   (self.steps[first_implication_formula_number]).formula,
                                                   (self.steps[second_implication_formula_number]).formula)
            if not current_cs[0]:
                current_cs = ConditionalSyllogism.rule(ConditionalSyllogism(),
                                                       (self.steps[second_implication_formula_number]).formula,
                                                       (self.steps[first_implication_formula_number]).formula)
            if not current_cs[0]:
                return None
        except IndexError:
            return None
        else:
            current_formula = current_cs[1]
            current_formula = Utils.formula_re_formatter(current_formula)
            step.formula = current_formula
        return step

    def __check_end(self) -> None:
        """
        Checks if the consequence_formula appears in the steps.formula
        If it appears, then it means that it is a consequence formula, and the proving method can end,
        otherwise the method may continue.
        """
        for formula in self.formula_set:
            if formula == self.consequence_formula:
                self.end = True
                return
        for step in self.steps:
            if self.consequence_formula == step.formula:
                self.end = True
                return
        self.end = False

    def __steps_append(self, step: Step) -> bool:
        """
        Appending to self steps list, if it's possible, if step id contained by steps, returns False, otherwise True
        If the step is None, return False

        Args:
            step: step will be appended if possible
        Returns:
             whether to append was successful or not
        """
        if step is None:
            return False
        if not isinstance(step, Step):
            return False
        counter = 0
        step_id = step.step_id
        for current_step in self.steps:
            counter += 1
            if current_step.step_id == step_id:
                return False
            if current_step.formula == step.formula:
                raise FormulaInStepsException
        if counter != step_id:
            return False

        self.steps.append(step)
        return True

    def new(self, formula_set: list, consequence_formula: str) -> None:
        """
        New proving method helper.

        Args:
            formula_set: list of logical formulas, as string, hypothesis
            consequence_formula: consequence logical formula, that will should be proved
        """
        self.__init__(formula_set, consequence_formula)

    def get_formula_set_consequence_concat(self) -> str:
        """
        Concat into one string all the formula in formula_set and consequence_formula
        Example:
            formula_set = ['X', 'Y', '(X >> Y)']
            consequence_formula = '~X'
            concat = '{X, Y, (X >> Y)} |- ~X'

        Returns:
            Concat of strings
        """
        if self.formula_set == [] or self.formula_set == ['']:
            concat = '{ } |- ' + self.consequence_formula
        else:
            concat = ', '.join(self.formula_set)
            concat = '{' + concat + '} |- ' + self.consequence_formula
        return str(concat)

    def get_steps_string(self) -> list:
        """
        Runs through self steps and generates a list of strings. Strings contains all data from each step.

        Returns:
            steps (list of strings) contains string that represents model steps.
        """
        steps = []
        for step in self.steps:
            if step.action == Actions.HYP:
                current_step = str(step.step_id + 1) + '. ' + str(step.formula) + ' [HYP]'
                steps.append(current_step)
            elif step.action == Actions.AXIOM:
                current_step = str(step.step_id + 1) + '. ' + str(step.formula) + ' ' + step.axiom_details
                steps.append(current_step)
            elif step.action == Actions.MP:
                current_step = (str(step.step_id + 1) + '. ' + str(step.formula) + ' [MP(' + str(
                    step.rule_implication + 1) + ',' + str(step.rule_detached + 1) + ')]')
                steps.append(current_step)
            elif step.action == Actions.MT:
                current_step = (str(step.step_id + 1) + '. ' + str(step.formula) + ' [MT(' + str(
                    step.rule_implication + 1) + ',' + str(step.rule_detached + 1) + ')]')
                steps.append(current_step)
            elif step.action == Actions.MTP:
                current_step = (str(step.step_id + 1) + '. ' + str(step.formula) + ' [MTP(' + str(
                    step.rule_implication + 1) + ',' + str(step.rule_detached + 1) + ')]')
                steps.append(current_step)
            elif step.action == Actions.MPT:
                current_step = (str(step.step_id + 1) + '. ' + str(step.formula) + ' [MPT(' + str(
                    step.rule_implication + 1) + ',' + str(step.rule_detached + 1) + ')]')
                steps.append(current_step)
            elif step.action == Actions.CS:
                current_step = (str(step.step_id + 1) + '. ' + str(step.formula) + ' [CS(' + str(
                    step.rule_implication + 1) + ',' + str(step.rule_detached + 1) + ')]')
                steps.append(current_step)
            else:
                return []
        return steps

    def get_hint(self) -> (bool, str, str):
        """
        Gives hint, that is there any new option to execute the Modus Ponens rule

        Returns:
            Tuple of (success_flag, implication, detached).
            success_flag is a boolean indicating whether there is possible modus ponens rule usage
            implication: implication formula for modus ponens rule
            detached: detached formula for modus ponens rule
        """
        if self.end:
            return False, '', ''
        for implication in self.steps:
            for detached in self.steps:
                current_mp = list(ModusPonens.rule(ModusPonens(), implication.formula, detached.formula))
                current_mt = list(ModusTollens.rule(ModusTollens(), implication.formula, detached.formula))
                current_mtp = list(
                    ModusTollendoPonens.rule(ModusTollendoPonens(), implication.formula, detached.formula))
                current_mpt = list(
                    ModusPonendoTollens.rule(ModusPonendoTollens(), implication.formula, detached.formula))
                current_cs = list(
                    ConditionalSyllogism.rule(ConditionalSyllogism(), implication.formula, detached.formula))
                if current_mp[0]:
                    formula_in_set = False
                    for formula in self.steps:
                        if Utils.formula_re_formatter(current_mp[1]) == formula.formula:
                            formula_in_set = True
                            break
                    if not formula_in_set:
                        return True, implication.formula, detached.formula
                elif current_mt[0]:
                    formula_in_set = False
                    for formula in self.steps:
                        if Utils.formula_re_formatter(current_mt[1]) == formula.formula:
                            formula_in_set = True
                            break
                    if not formula_in_set:
                        return True, implication.formula, detached.formula
                elif current_mtp[0]:
                    formula_in_set = False
                    for formula in self.steps:
                        if Utils.formula_re_formatter(current_mtp[1]) == formula.formula:
                            formula_in_set = True
                            break
                    if not formula_in_set:
                        return True, implication.formula, detached.formula
                elif current_mpt[0]:
                    formula_in_set = False
                    for formula in self.steps:
                        if Utils.formula_re_formatter(current_mpt[1]) == formula.formula:
                            formula_in_set = True
                            break
                    if not formula_in_set:
                        return True, implication.formula, detached.formula
                elif current_cs[0]:
                    formula_in_set = False
                    for formula in self.steps:
                        if Utils.formula_re_formatter(current_cs[1]) == formula.formula:
                            formula_in_set = True
                            break
                    if not formula_in_set:
                        return True, implication.formula, detached.formula
                else:
                    continue
        return False, '', ''

    def delete_steps(self, index: int) -> bool:
        """
        Deletes steps from model steps, from the given index to the end of the steps list.

        Args:
            index: index of the element.
        Returns:
            True if the deletion was successful
            False otherwise
        """
        if not isinstance(index, int):
            return False
        if len(self.steps) == 0:
            return False
        if not (0 <= index < len(self.steps)):
            return False

        del self.steps[index:]
        self.number_of_steps = len(self.steps)
        self.__check_end()
        return True

    def add_axiom(self, formula: str) -> bool:
        """
        Adding formulas to the self added_formula, if the formula is tautology and not in self base_formulas.

        Args:
            formula: input formula that will be added.
        Returns:
            True if the addition was successful
            False otherwise
        """
        if not isinstance(formula, str):
            return False
        if not Utils.is_valid_formula(formula):
            return False
        if not Utils.check_brackets(formula):
            return False
        formula_reader = FormulaReader()
        if not formula_reader.is_tautology(formula):
            return False
        if formula in self.base_axioms:
            return False
        if formula in self.added_axioms:
            return False
        self.added_axioms.append(Utils.formula_re_formatter(formula))
        return True

    def action_added_axiom(self, formula: str, data: list) -> bool:
        """
        Tries to add the current_step to steps, if possible.
        Tries to complete action_axiom with base_axiom = False param

        Args:
            formula: logical added axiom formula
            data: list of logical formula strings. List length must be exactly the same as how many
                variable are in the current step's formula.
        Returns:
            False if adding step was unsuccessful
            Otherwise True
        """
        try:
            current_step = Step(self.number_of_steps, formula, Actions.AXIOM, rule_implication=0, rule_detached=0)
        except ValueError:
            return False

        current_step = self.__action_axiom(current_step, data, base_axiom=False)
        if current_step is None:
            return False

        if not self.__steps_append(current_step):
            return False
        self.number_of_steps += 1
        self.__check_end()
        return True

    def formula_set_contains_tautology(self) -> bool:
        """
        Searches for tautologies in the formula set.

        Returns:
            True if the formula set contains a tautology.
            Otherwise False
        """
        formula_reader = FormulaReader()
        for formula in self.formula_set:
            if formula_reader.is_tautology(formula):
                return True
        return False

    def delete_tautologies(self) -> bool:
        """
        Deletes all tautologies from the formula set.

        Returns:
             True if the deletion was successful
             Otherwise False
        """
        if not self.formula_set_contains_tautology():
            return False

        current_list = []
        formula_reader = FormulaReader()
        for formula in self.formula_set:
            if not formula_reader.is_tautology(formula):
                current_list.append(formula)
        self.formula_set = []
        self.formula_set = current_list
        return True

    def task_is_provable(self) -> bool:
        """
        Creates a conjunction chain of the formulas in formula set, and the negated consequence formula.
        If this formula is negated, and the negated formula is tautology, according to logic, the consequence is
        provable.

        Returns:
            True if the task is provable
            False otherwise
        """
        if not self.formula_set:
            return True

        task = ''
        for formula in self.formula_set:
            task = task + formula
            task = task + ' & '

        task = '~(' + task + '(~' + self.consequence_formula + '))'

        formula_reader = FormulaReader()
        if formula_reader.is_tautology(task):
            return True
        else:
            return False

    def save_model(self) -> bool:
        """
        Tries to save all data of the current model

        Returns:
            True if the saving was successful
            False otherwise
        """
        steps = []
        for step in self.steps:
            if step.action == Actions.HYP:
                steps.append([step.step_id, step.formula, 'Actions.HYP', '', 0, 0])
            elif step.action == Actions.AXIOM:
                steps.append([step.step_id, step.formula, 'Actions.AXIOM', step.axiom_details, 0, 0])
            elif step.action == Actions.MP:
                steps.append([step.step_id, step.formula, 'Actions.MP', '', step.rule_implication, step.rule_detached])
            elif step.action == Actions.MT:
                steps.append([step.step_id, step.formula, 'Actions.MT', '', step.rule_implication, step.rule_detached])
            elif step.action == Actions.MTP:
                steps.append([step.step_id, step.formula, 'Actions.MTP', '', step.rule_implication, step.rule_detached])
            elif step.action == Actions.MPT:
                steps.append([step.step_id, step.formula, 'Actions.MPT', '', step.rule_implication, step.rule_detached])
            elif step.action == Actions.CS:
                steps.append([step.step_id, step.formula, 'Actions.CS', '', step.rule_implication, step.rule_detached])
            else:
                return False

        data = {
            'formula_set': self.formula_set,
            'consequence_formula': self.consequence_formula,
            'end': self.end,
            'number_of_steps': self.number_of_steps,
            'steps': steps,
            'task_name': self.get_formula_set_consequence_concat(),
            'added_axioms': self.added_axioms
        }
        try:
            self.__data_access.save_model(data)
            return True
        except OSError:
            return False

    def load_model(self, path: str) -> bool:
        """
        Tries to load a model, from a json file (with the given specific path).
        Sets all model data from the json. Appending every step from the file after checking,
         whether it is valid addition.

        Args:
            path: full path to json file that contains data to load.

        Returns:
            True if loading was successful
            False otherwise
        """
        try:
            data = self.__data_access.load_model(path)
        except OSError:
            return False

        try:
            self.__input_checker(data['formula_set'], data['consequence_formula'])
            self.formula_set = data['formula_set']
            self.consequence_formula = Utils.formula_re_formatter(data['consequence_formula'])
            self.steps = []
            self.number_of_steps = data['number_of_steps']
            self.end = data['end']
            self.added_axioms = data['added_axioms']
            for step in data['steps']:
                current_step = list(step)
                if current_step[2] == 'Actions.HYP':
                    if not current_step[1] in self.formula_set:
                        raise ValueError
                    if not self.__steps_append(Step(current_step[0], current_step[1], Actions.HYP)):
                        raise ValueError
                elif current_step[2] == 'Actions.AXIOM':
                    formula_reader = FormulaReader()
                    if not formula_reader.is_tautology(current_step[1]):
                        raise ValueError
                    if not self.__steps_append(
                            Step(current_step[0], current_step[1], Actions.AXIOM, axiom_details=current_step[3])):
                        raise ValueError
                elif current_step[2] == 'Actions.MP':
                    if not ModusPonens.rule(ModusPonens(), self.steps[current_step[4]].formula, self.steps[current_step[5]].formula)[0]:
                        raise ValueError
                    if not self.__steps_append(
                            Step(current_step[0], current_step[1], Actions.MP, '', current_step[4], current_step[5])):
                        raise ValueError
                elif current_step[2] == 'Actions.MT':
                    if not ModusTollens.rule(ModusTollens(), self.steps[current_step[4]].formula, self.steps[current_step[5]].formula)[0]:
                        raise ValueError
                    if not self.__steps_append(
                            Step(current_step[0], current_step[1], Actions.MT, '', current_step[4], current_step[5])):
                        raise ValueError
                elif current_step[2] == 'Actions.MTP':
                    if not ModusTollendoPonens.rule(ModusTollendoPonens(), self.steps[current_step[4]].formula, self.steps[current_step[5]].formula)[0]:
                        raise ValueError
                    if not self.__steps_append(
                            Step(current_step[0], current_step[1], Actions.MTP, '', current_step[4], current_step[5])):
                        raise ValueError
                elif current_step[2] == 'Actions.MPT':
                    if not ModusPonendoTollens.rule(ModusPonendoTollens(), self.steps[current_step[4]].formula, self.steps[current_step[5]].formula)[0]:
                        raise ValueError
                    if not self.__steps_append(
                            Step(current_step[0], current_step[1], Actions.MPT, '', current_step[4], current_step[5])):
                        raise ValueError
                elif current_step[2] == 'Actions.CS':
                    if not ConditionalSyllogism.rule(ConditionalSyllogism(), self.steps[current_step[4]].formula, self.steps[current_step[5]].formula)[0]:
                        raise ValueError
                    if not self.__steps_append(
                            Step(current_step[0], current_step[1], Actions.CS, '', current_step[4], current_step[5])):
                        raise ValueError
                else:
                    raise ValueError
            if self.number_of_steps != len(self.steps):
                raise ValueError
        except ValueError:
            raise ValueError
        except Exception:
            raise Exception
        return True
