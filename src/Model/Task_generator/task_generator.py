import random

from Model.formula_reader import FormulaReader


class TaskGenerator:
    @staticmethod
    def generate_task(number_of_formula_in_formula_set: int, variables: list) -> tuple:
        """
        Tries to generate a task.
        The number of the formula set will be the number_of_formula_in_formula_set (can be zero).
        For ach formula in the set, and for the consequence formula as well, the generate_formula will be called.

        Args:
            number_of_formula_in_formula_set: this amount of formulas will be in the formula set.
            variables: list of variables, that will be in the formulas

        Returns:
            A tuple, that contains the formula set, and the consequence formula
        """
        while True:
            formula_set = []
            for i in range(number_of_formula_in_formula_set):
                formula_set.append(TaskGenerator.__generate_formula(variables))

            consequence_formula = TaskGenerator.__generate_formula(variables)

            if TaskGenerator.__task_is_provable(formula_set, consequence_formula):
                break
        return formula_set, consequence_formula

    @staticmethod
    def __generate_formula(variables: list) -> str:
        """
        Uses the variable list, and tries to generate a formula, that contains 1 to 5 variables, and operations between
        the variables.

        Args:
            variables: Contains the variables for the formulas

        Returns:
            A logical formula
        """
        formula_length = random.randint(0, 4)
        formula = '('

        for i in range(formula_length + 1):
            negation = random.randint(0, 5)
            if negation == 0:
                formula = formula + '~'
            variable = random.randint(0, len(variables) - 1)
            formula = formula + variables[variable]

            if i != formula_length:
                formula = formula + ' '
                operation = random.randint(0, 3)
                if operation == 0:
                    formula = formula + '>> '
                elif operation == 1:
                    formula = formula + '| '
                elif operation == 2:
                    formula = formula + '& '
        formula = formula + ')'

        return formula

    @staticmethod
    def __task_is_provable(formula_set: list, consequence_formula: str) -> bool:
        """
        Creates a conjunction chain of the formulas in formula set, and the negated consequence formula.
        If this formula is negated, and the negated formula is tautology, according to logic, the consequence is
        provable.

        Returns:
            True if the task is provable
            False otherwise
        """
        if not formula_set:
            return True
        task = ''
        for formula in formula_set:
            task = task + formula
            task = task + ' & '

        task = '~(' + task + '(~' + consequence_formula + '))'

        formula_reader = FormulaReader()
        if formula_reader.is_tautology(task):
            return True
        else:
            return False
