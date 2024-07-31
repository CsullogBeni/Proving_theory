import re
import unittest
from Model.Utils.utils import Utils


class UnitTestUtils(unittest.TestCase):
    """
    Unit test for Model.Utils.utils.py. Testing all helper functions and tools
    """

    def test_is_valid_formula(self) -> None:
        """
        Testing the is_valid_formula function can decide a formula is valid or not.
        """
        self.assertTrue(Utils.is_valid_formula("(A >> (B >> A))"))
        self.assertTrue(Utils.is_valid_formula("(A >> (B >> C)) >> ((A >> B) >> (A >> C))"))
        self.assertTrue(Utils.is_valid_formula("(~A >> B) >> ((~A >> ~B) >> A)"))
        self.assertTrue(Utils.is_valid_formula(""))
        self.assertTrue(Utils.is_valid_formula("(A >> (B >> A))"))
        self.assertTrue(Utils.is_valid_formula("(A >> (C >> D))"))

        self.assertFalse(Utils.is_valid_formula("A ~ B"))
        self.assertFalse(Utils.is_valid_formula("A << B"))
        self.assertFalse(Utils.is_valid_formula("A & & B"))
        self.assertFalse(Utils.is_valid_formula("A B"))

        self.assertFalse(Utils.is_valid_formula("S"))
        self.assertFalse(Utils.is_valid_formula("(S >> (B >> A))"))
        self.assertFalse(Utils.is_valid_formula("(A >> (S >> A))"))

        self.assertFalse(Utils.is_valid_formula("A v B"))
        self.assertFalse(Utils.is_valid_formula("A yx B"))
        self.assertFalse(Utils.is_valid_formula("A _ B"))

    def test_formula_re_formatter(self) -> None:
        """
        Unit tests for Model.Utils.utils.formula_re_formatter
        """
        self.assertEqual(Utils.formula_re_formatter("(A>>(B>>A))"), "(A >> (B >> A))")
        self.assertEqual(Utils.formula_re_formatter("~A"), "~A")
        self.assertEqual(Utils.formula_re_formatter("(A&(B|A))"), "(A & (B | A))")
        self.assertEqual(Utils.formula_re_formatter(" ( A >> ( B >> A ) )"), "(A >> (B >> A))")

        self.assertNotEqual(Utils.formula_re_formatter("(A>>(B>>A))"), "(A >> (B >>A ))")
        self.assertNotEqual(Utils.formula_re_formatter("( A>> (B >> A) ) "), "(A >> (B >>A ))")

    def test_get_formula_variables(self) -> None:
        """
        Unit tests for Model.Utils.utils.get_formula_variables
        """
        self.assertEqual(Utils.get_formula_variables('A >> B'), ['A', 'B'])
        self.assertEqual(Utils.get_formula_variables('A | B | C'), ['A', 'B', 'C'])
        self.assertEqual(Utils.get_formula_variables('A & B & C | D'), ['A', 'B', 'C', 'D'])

        with self.assertRaises(ValueError):
            Utils.get_formula_variables('')
            Utils.get_formula_variables('A << B')
            Utils.get_formula_variables('a')
            Utils.get_formula_variables('A | b')

    def test_bind_variables_to_substitution_data(self) -> None:
        """
        Unit tests for Model.Utils.utils.bind_variable_to_substitution_data
        """
        list_of_variables = ['A', 'B']
        data = ['(C >> D)', '(D >> C)']
        self.assertEqual(Utils.bind_variables_to_substitution_data(list_of_variables, data),
                         {'A': '(C >> D)', 'B': '(D >> C)'})
        list_of_variables = ['A', 'B', 'C']
        data = ['(C >> D)', '(D >> C)', '((A | B) >> C)']
        self.assertEqual(Utils.bind_variables_to_substitution_data(list_of_variables, data),
                         {'A': '(C >> D)', 'B': '(D >> C)', 'C': '((A | B) >> C)'})

        with self.assertRaises(ValueError):
            list_of_variables = ['A', 'B']
            data = ['(C >> D)', '(D >> )']
            Utils.bind_variables_to_substitution_data(list_of_variables, data)
            list_of_variables = ['(A)', 'B']
            data = ['(C >> D)', '(D >> C)']
            Utils.bind_variables_to_substitution_data(list_of_variables, data)
            list_of_variables = ['>>', 'B']
            data = ['(C >> D)', '(D >> C)']
            Utils.bind_variables_to_substitution_data(list_of_variables, data)
            list_of_variables = ['A', 'B']
            data = ['(C >> D)', 'D >> C']
            Utils.bind_variables_to_substitution_data(list_of_variables, data)

    def test_replace_function(self) -> None:
        """
        Unit tests for Model.Utils.utils.replace_function
        """
        binded_dictionary = {'A': '(C >> D)', 'B': '(D >> C)'}
        pattern = re.compile('|'.join(re.escape(key) for key in binded_dictionary.keys()))
        match = pattern.search('A')
        self.assertEqual(Utils.replace_function(match, binded_dictionary), '(C >> D)')
        match = pattern.search('B')
        self.assertEqual(Utils.replace_function(match, binded_dictionary), '(D >> C)')

        with self.assertRaises(ValueError):
            Utils.replace_function(match, "string")
            Utils.replace_function("A", binded_dictionary)

    def test_replace_in_formula(self) -> None:
        """
        Unit tests for Model.Utils.utils.replace_in_formula
        """
        formula = '(A >> B)'
        binded_list = {'A': '(C >> D)', 'B': '(D >> C)'}
        self.assertEqual(Utils.replace_in_formula(formula, binded_list), '((C >> D) >> (D >> C))')
        formula = '((A >> B) >> A)'
        binded_list = {'A': '(C >> D)', 'B': '(D >> C)'}
        self.assertEqual(Utils.replace_in_formula(formula, binded_list), '(((C >> D) >> (D >> C)) >> (C >> D))')

        with self.assertRaises(ValueError):
            Utils.replace_in_formula(1, binded_list)
            Utils.replace_in_formula(formula, '')
            formula = '((A >> B) >> C)'
            binded_list = {'A': '(C >> D)', 'B': '(D >> C)'}
            Utils.replace_in_formula(formula, binded_list)

    def test_check_brackets(self) -> None:
        """
        Unit tests for Model.Utils.utils.check_brackets
        """
        self.assertTrue(Utils.check_brackets("(A >> (B >> A))"))
        self.assertTrue(Utils.check_brackets("((A >> (B >> C)) >> ((A >> B) >> (A >> C)))"))
        self.assertTrue(Utils.check_brackets("((~A >> B) >> ((~A >> ~B) >> A))"))
        self.assertTrue(Utils.check_brackets("(A >> A)"))
        self.assertTrue(Utils.check_brackets("((A >> B) >> ((B >> C) >> (A >> C)))"))
        self.assertTrue(Utils.check_brackets("(A >> ~~A)"))
        self.assertTrue(Utils.check_brackets("(~~A >> A)"))
        self.assertTrue(Utils.check_brackets("((A >> B) >> (~~A >> ~~B))"))
        self.assertTrue(Utils.check_brackets("(A >> (B >> (A & B)))"))
        self.assertTrue(Utils.check_brackets("((A & B) >> A)"))
        self.assertTrue(Utils.check_brackets("((A & B) >> B)"))
        self.assertTrue(Utils.check_brackets("(B >> (A | B))"))
        self.assertTrue(Utils.check_brackets("(A >> (A | B))"))
        self.assertTrue(Utils.check_brackets("((A >> C) >> ((B >> C) >> ((A | B) >> C)))"))
        self.assertTrue(Utils.check_brackets("((A >> C) >> ((B >> C) >> ((A | B) >> ~C)))"))

        self.assertTrue(Utils.check_brackets("(~~A >> A)"))
        self.assertTrue(Utils.check_brackets("(~~(A >> B) >> A)"))

        self.assertTrue(Utils.check_brackets("~A"))
        self.assertTrue(Utils.check_brackets("~(A | B)"))

        self.assertFalse(Utils.check_brackets("(~(~((A >> B))) >> A"))
        self.assertFalse(Utils.check_brackets("(~(~(A >> B)) >> A"))


if __name__ == "__main__":
    unittest.main()
