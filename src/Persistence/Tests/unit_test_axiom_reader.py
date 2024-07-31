import unittest
import Persistence
from Persistence.axiom_reader import AxiomReader


class UnitTestAxiomReader(unittest.TestCase):
    """
    Unit test for Persistence.AxiomReader class.

    Methods:
        test_axiom_reader - Initialize an AxiomReader, and run tests.

    """
    def test_axiom_reader(self) -> None:
        """
        Tests the functions in AxiomReader class.

        Reads all the axioms, that necessary, and check if the axioms list is empty.
        """
        axiom_reader = Persistence.axiom_reader.AxiomReader()
        axioms = axiom_reader.read_axioms_from_json()

        self.assertNotEqual(len(axioms), 0)
        self.assertIn("(A >> (B >> A))", axioms)
        self.assertIn( "((A >> (B >> C)) >> ((A >> B) >> (A >> C)))", axioms)
        self.assertIn("((~A >> B) >> ((~A >> ~B) >> A))", axioms)
        self.assertIn("(A >> A)", axioms)
        self.assertIn("((A >> B) >> ((B >> C) >> (A >> C)))", axioms)
        self.assertIn("(A >> ~~A)", axioms)
        self.assertIn("(~~A >> A)", axioms)
        self.assertIn("((A >> B) >> (~~A >> ~~B))", axioms)
        self.assertIn("(A >> (B >> (A & B)))", axioms)
        self.assertIn("((A & B) >> A)", axioms)
        self.assertIn("((A & B) >> B)", axioms)
        self.assertIn("(B >> (A | B))", axioms)
        self.assertIn("(A >> (A | B))", axioms)
        self.assertIn("((A >> C) >> ((B >> C) >> ((A | B) >> C)))", axioms)


if __name__ == "__main__":
    unittest.main()
