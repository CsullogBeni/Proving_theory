import ast
import re
import tokenize

import sympy

import Persistence.data_access


class Utils:
    """
    Contains function that are in use various files and classes. Helpful functions for avoiding redundant codes.
    """
    @staticmethod
    def is_valid_formula(formula_string: str) -> bool:
        """
        Checks whether the input formula is valid logical formula, or not.
        If not, the sympy.parsing.sympy_parser.parse_expr() throws exception.
        Formula cannot contain the letter 'S' due to sympy.parse_expr. This function converts S to a local dictionary
        in the formula_string

        Args:
            formula_string (str): a string logical formula
        Returns:
            If the formula is valid formula, return True, otherwise False.
        """
        if not isinstance(formula_string, str):
            return False
        if formula_string == '':
            return True
        acceptable_characters = set('ABCDFGHJKLMWRTZU ()>|&~')
        for char in formula_string:
            if char not in acceptable_characters:
                return False

        if ' > ' in formula_string:
            return False
        if '&&' in formula_string:
            return False
        if '||' in formula_string:
            return False
        if '<<' in formula_string:
            return False
        try:
            sympy.parse_expr(formula_string)
            return True
        except (sympy.SympifyError, TypeError, SyntaxError, tokenize.TokenError):
            return False

    @staticmethod
    def formula_re_formatter(formula: str) -> str:
        """
        Re-formats logical formula. Firstly remove all spaces, after that insert spaces around binary operations.

        Args:
            formula (str): a logical formula string
        Returns:
            reformatted formula
        """
        formula = formula.strip()
        formula = formula.replace(' ', '')
        formula = formula.replace('|', ' | ')
        formula = formula.replace('&', ' & ')
        formula = formula.replace('>>', ' >> ')
        return formula

    @staticmethod
    def get_formula_variables(formula: str) -> list:
        """
        Gets all variables from a logical formula

        Args:
            formula (str): logical formula
        Returns:
            set of characters, set of variables
        """
        if not Utils.is_valid_formula(formula):
            raise ValueError
        list_of_variables = set(re.findall(r'\b[A-Z]\b', formula))
        return sorted(list_of_variables)

    @staticmethod
    def bind_variables_to_substitution_data(list_of_variables: list, data: list) -> dict:
        """
        The function generates a dictionary of tle list of variables and the data. It binds together.
        length of the two input params must be equal.

        Raises
            ValueError: if one of the input formulas are invalid, or the length of the two input params
                                are different

        Args:
            list_of_variables: a list that contains all the variables in a logical formula
            data: a list, that contains the formulas, that will be substituted into the variables

        Returns:
             the generated dictionary
        """
        if len(list_of_variables) != len(data):
            raise ValueError

        for formula in list_of_variables:
            if not Utils.is_valid_formula(formula):
                raise ValueError
            if not Utils.check_brackets(formula):
                raise ValueError

        for formula in data:
            if not Utils.is_valid_formula(formula):
                raise ValueError
            if not Utils.check_brackets(formula):
                raise ValueError

        binded_list = list(zip(list_of_variables, data))
        return {val: replace_data for val, replace_data in binded_list}

    @staticmethod
    def replace_function(match: re.Match, binded_dict: dict) -> dict:
        """
        The function searches the key equals match in the binded_list and returns that value.

        Args:
            match: key to be searched
            binded_dict: dictionary that contains keys and values
        Returns:
            a key's value
        """
        if not isinstance(match, re.Match):
            raise ValueError
        if not isinstance(binded_dict, dict):
            raise ValueError

        return binded_dict[match.group(0)]

    @staticmethod
    def replace_in_formula(formula: str, binded_dictionary: dict) -> str:
        """
        The function changes the keys in the formula to tha value in binded_list
        re.compile generates a string that contains the dictionary keys, separated wit '|'
        pattern.sub changes the dictionary values into the formula simultaneously.

        Args:
            formula: logical formula
            binded_dictionary: contains the formula's variables and their replacing values

        Returns:
             the original formula, but the variables replaced with the dictionary values
        """
        if not isinstance(formula, str):
            raise ValueError
        if not isinstance(binded_dictionary, dict):
            raise ValueError

        for key, value in binded_dictionary.items():
            if key not in formula:
                raise ValueError

        try:
            pattern = re.compile('|'.join(re.escape(key) for key in binded_dictionary.keys()))
            result = pattern.sub(lambda match: Utils.replace_function(match, binded_dictionary), formula)
        except ValueError:
            raise ValueError
        return result

    @staticmethod
    def check_brackets(formula: str) -> bool:
        """
        Checking whether the formula's brackets are correct or not.

        Args:
            formula (str): string of the logical formula
        Returns:
            True if the brackets are correct
            False otherwise
        """
        if not isinstance(formula, str):
            return False
        formula = Utils.formula_re_formatter(formula)

        if len(formula) == 0:
            return True

        try:
            ast.parse(formula)
        except SyntaxError:
            return False

        operations = 0
        operations += (formula.count('>>') * 2)
        operations += (formula.count('|') * 2)
        operations += (formula.count('&') * 2)

        operations = operations - len(re.findall(r'\b[A-Z]\b', formula))

        if formula.count('(') != (operations + 1):
            return False
        if formula.count(')') != (operations + 1):
            return False

        return True

    @staticmethod
    def saving_new_proving_method_config(formula_set_string: str,
                                         consequence_formula: str) -> bool:
        """
        Splits formula_set_string. Checking each formula whether there are valid logical formulas or not.
        Checking formulas' brackets, if the brackets are incorrect, the function returns. Then tries to save the
        formula_set and consequence_formula to Persistence.

        Args:
            formula_set_string: string of formulas in formula set (split by ',')
            consequence_formula: string of the consequence formula

        Returns:
            True if saving was completed
            False if something went wrong (Incorrect params, or uncompleted saving).
        """
        if not isinstance(formula_set_string, str) and formula_set_string != []:
            return False
        if not isinstance(consequence_formula, str):
            return False

        if consequence_formula == "" or consequence_formula is None:
            return False

        if formula_set_string:
            formula_set_string = formula_set_string.replace(' ', '')
            formula_set_string = formula_set_string.replace('\t', '')
            formula_set_string = formula_set_string.replace('\n', '')
            formula_set = formula_set_string.split(',')
        else:
            formula_set = []

        for formula in formula_set:
            if not isinstance(formula, str):
                return False
            formula = Utils.formula_re_formatter(formula)
            if not Utils.is_valid_formula(formula):
                return False
            if not Utils.check_brackets(formula):
                return False

        if not isinstance(consequence_formula, str):
            return False
        consequence_formula = Utils.formula_re_formatter(consequence_formula)
        if not Utils.is_valid_formula(consequence_formula):
            return False
        if not Utils.check_brackets(consequence_formula):
            return False

        reformated_formula_set = []
        for formula in formula_set:
            if formula != '':
                reformated_formula_set.append(Utils.formula_re_formatter(formula))
        reformated_consequence_formula = Utils.formula_re_formatter(consequence_formula)

        try:
            data_access = Persistence.data_access.DataAccess()
            data_access.save_new_proving_method_config_window(reformated_formula_set, reformated_consequence_formula)
        except OSError:
            return False
        except ValueError:
            return False
        return True

    @staticmethod
    def load_new_proving_method_config() -> (list, str):
        """
        Loading formula_set, consequence formulas, that saved with  saving_new_proving_method_config

        Raises:
            OSError if the function can't read file
            ValueError if there are invalid formulas in the file

        Returns
            tuple of formula_set and consequence_formula
        """
        try:
            data_access = Persistence.data_access.DataAccess()
            formulas = data_access.load_new_proving_method_config_window()
        except OSError:
            raise OSError

        formula_set = formulas[0]
        consequence_formula = formulas[1]

        if consequence_formula == "" or consequence_formula is None:
            raise ValueError

        for formula in formula_set:
            if not isinstance(formula, str):
                raise ValueError
            formula = Utils.formula_re_formatter(formula)
            if not Utils.is_valid_formula(formula):
                raise ValueError
            if not Utils.check_brackets(formula):
                raise ValueError

        if not isinstance(consequence_formula, str):
            raise ValueError
        consequence_formula = Utils.formula_re_formatter(consequence_formula)
        if not Utils.is_valid_formula(consequence_formula):
            raise ValueError
        if not Utils.check_brackets(consequence_formula):
            raise ValueError

        return formulas
