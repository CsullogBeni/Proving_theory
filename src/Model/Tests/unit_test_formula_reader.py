import unittest
import Model
from Model.formula_reader import FormulaReader


class UnitTestAxiomReader(unittest.TestCase):
    """
    Unit test for Model.formula_reader.FormulaReader class.

    Methods:
        test_formula_reader: Initialize an FormulaReader, and run tests.

    """
    def test_axiom_reader(self) -> None:
        """
        Tests the functions in FormulaReader class.

        Testing is_tautology function with several tautologies, with formulas that can be satisfied
        and formulas that can't be satisfied.
        """
        formula_reader = Model.formula_reader.FormulaReader()

        self.assertTrue(formula_reader.is_tautology("(A >> (B >> A))"))
        self.assertTrue(formula_reader.is_tautology("(A >> (B >> C)) >> ((A >> B) >> (A >> C))"))
        self.assertTrue(formula_reader.is_tautology("(~A >> B) >> ((~A >> ~B) >> A)"))
        self.assertTrue(formula_reader.is_tautology("(A >> A)"))
        self.assertTrue(formula_reader.is_tautology("(A >> B) >> ((B >> C) >> (A >> C))"))
        self.assertTrue(formula_reader.is_tautology("(A >> (~~A))"))
        self.assertTrue(formula_reader.is_tautology("((~~A) >> A)"))
        self.assertTrue(formula_reader.is_tautology("(A >> B) >> (~~A >> ~~B)"))
        self.assertTrue(formula_reader.is_tautology("A >> (B >> (A & B))"))
        self.assertTrue(formula_reader.is_tautology("(A & B) >> A"))
        self.assertTrue(formula_reader.is_tautology("(A & B) >> B"))
        self.assertTrue(formula_reader.is_tautology("B >> (A | B)"))
        self.assertTrue(formula_reader.is_tautology("A >> (A | B)"))
        self.assertTrue(formula_reader.is_tautology("(A >> C) >> ((B >> C) >> (A | B >> C))"))
        self.assertTrue(formula_reader.is_tautology("(A >> A)"))

        self.assertFalse(formula_reader.is_tautology("A >> (B | B)"))
        self.assertFalse(formula_reader.is_tautology("A >> B"))
        self.assertFalse(formula_reader.is_tautology("(A | A) >> (B | B)"))
        self.assertFalse(formula_reader.is_tautology("(A & C) >> (B | B)"))
        self.assertFalse(formula_reader.is_tautology("(A >> A) >> B"))
        self.assertFalse(formula_reader.is_tautology("~(B >> (A | B))"))
        self.assertFalse(formula_reader.is_tautology(""))


if __name__ == "__main__":
    unittest.main()
