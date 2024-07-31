import unittest
from Model.Rules.modus_ponendo_tollens import ModusPonendoTollens


class UnitTestModusTollendoPonens(unittest.TestCase):
    """
    Unit test for Model.Rules.modus_tollendo_ponens.ModusTollendoPonens class
    """

    def test_modus_ponens(self) -> None:
        """
        Testing rule function
        """
        self.assertEqual(ModusPonendoTollens.rule(ModusPonendoTollens(), '(A >> B)', 'C'), (False, ''))
        self.assertEqual(ModusPonendoTollens.rule(ModusPonendoTollens(), '(A >> B)', ''), (False, ''))
        self.assertEqual(ModusPonendoTollens.rule(ModusPonendoTollens(), '', ''), (False, ''))
        self.assertEqual(ModusPonendoTollens.rule(ModusPonendoTollens(), '(A >> B)', '~(A >> B)'), (False, ''))
        self.assertEqual(ModusPonendoTollens.rule(ModusPonendoTollens(), '(A | B)', '(A >> A >> B)'), (False, ''))

        self.assertEqual(ModusPonendoTollens.rule(ModusPonendoTollens(), '(~A >> ~B)', 'B'), (True, 'A'))
        self.assertEqual(
            ModusPonendoTollens.rule(ModusPonendoTollens(), '(~(B >> C) >> ~(A >> (B >> C)))', '(A >> (B >> C))'),
            (True, '(B>>C)'))
        self.assertEqual(
            ModusPonendoTollens.rule(ModusPonendoTollens(), '(~(A >> (B >> C)) >> ~((A >> B) >> (A >> C)))',
                                     '((A >> B) >> (A >> C))'),
            (True, '(A>>(B>>C))'))


if __name__ == "__main__":
    unittest.main()
