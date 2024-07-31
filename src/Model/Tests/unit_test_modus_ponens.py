import unittest
from Model.Rules.modus_ponens import ModusPonens


class UnitTestModusPonens(unittest.TestCase):
    """
    Unit test for Model.Rules.modus_ponens.ModusPonens class
    """

    def test_modus_ponens(self) -> None:
        """
        Testing rule function
        """
        self.assertEqual(ModusPonens.rule(ModusPonens(), '(A >> B)', 'C'), (False, ''))
        self.assertEqual(ModusPonens.rule(ModusPonens(), '(A >> B)', ''), (False, ''))
        self.assertEqual(ModusPonens.rule(ModusPonens(), '', ''), (False, ''))
        self.assertEqual(ModusPonens.rule(ModusPonens(), '(A >> B)', '(A >> B)'), (False, ''))
        self.assertEqual(ModusPonens.rule(ModusPonens(), '(A >> B)', '(A >> A >> B)'), (False, ''))

        self.assertEqual(ModusPonens.rule(ModusPonens(), '(A >> B)', 'A'), (True, 'B'))
        self.assertEqual(ModusPonens.rule(ModusPonens(), '((B >> C) >> (A >> (B >> C)))', '(B >> C)'),
                         (True, '(A>>(B>>C))'))
        self.assertEqual(
            ModusPonens.rule(ModusPonens(), '((A >> (B >> C)) >> ((A >> B) >> (A >> C)))', '(A >> (B >> C))'),
            (True, '((A>>B)>>(A>>C))'))


if __name__ == "__main__":
    unittest.main()
