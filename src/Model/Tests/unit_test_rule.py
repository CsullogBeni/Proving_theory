import unittest
from Model.Rules.rule import Rule


class UnitTestRule(unittest.TestCase):
    """
    Unit test for Model.Rules.Rule class

    Methods:
        test_is_implication_formula: testing is a formula an implication formula
    """

    def test_is_implication(self) -> None:
        """
        Testing the is_implication function, that can decide a formula is an implication formula or not.
        """
        self.assertTrue(Rule._is_implication('(A >> B)'))
        self.assertTrue(Rule._is_implication('((A >> B) >> (A >> B))'))
        self.assertTrue(Rule._is_implication('((A | B) >> (A | B))'))
        self.assertFalse(Rule._is_implication('(A | B)'))
        self.assertFalse(Rule._is_implication('(A & B)'))
        self.assertFalse(Rule._is_implication('~A'))
        self.assertFalse(Rule._is_implication(''))

    def test_is_negation(self) -> None:
        """
        Testing the is_negation function, that can decide a formula is a negation formula or not.
        """
        self.assertTrue(Rule.is_negation('~A'))
        self.assertTrue(Rule.is_negation('~(A >> B)'))
        self.assertTrue(Rule.is_negation('~(A | B)'))

        self.assertFalse(Rule.is_negation('(A >> B)'))
        self.assertFalse(Rule.is_negation('((A >> B) >> (A >> B))'))
        self.assertFalse(Rule.is_negation('((A | B) >> (A | B))'))
        self.assertFalse(Rule.is_negation('(A | B)'))
        self.assertFalse(Rule.is_negation('(A & B)'))
        self.assertFalse(Rule.is_negation(''))

    def test_contains_disjunction(self) -> None:
        """
        Unit test for Model.Rules.rule.test_disjunction function
        """
        self.assertFalse(Rule._contains_disjunction('~A'))
        self.assertFalse(Rule._contains_disjunction('~(A >> B)'))
        self.assertFalse(Rule._contains_disjunction(0))
        self.assertFalse(Rule._contains_disjunction('S'))
        self.assertFalse(Rule._contains_disjunction('((A)'))

        self.assertTrue(Rule._contains_disjunction('~(A | B)'))
        self.assertTrue(Rule._contains_disjunction('((A | B) >> (A | B))'))

    def test_input_checker(self) -> None:
        """
        Unit test for Model.Rules.rule.input_checker function
        """
        self.assertTrue(Rule._input_checker('(A >> B)', 'A'))
        self.assertTrue(Rule._input_checker('((A >> B) >> (A >> B))', 'A'))
        self.assertTrue(Rule._input_checker('((A | B) >> (A | B))', '(A >> B)'))

        self.assertFalse(Rule._input_checker('(A | B)', '(A >> B)'))
        self.assertFalse(Rule._input_checker('(A & B)', ''))


if __name__ == "__main__":
    unittest.main()
