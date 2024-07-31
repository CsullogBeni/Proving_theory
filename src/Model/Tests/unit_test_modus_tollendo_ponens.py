import unittest
from Model.Rules.modus_tollendo_ponens import ModusTollendoPonens


class UnitTestModusTollendoPonens(unittest.TestCase):
    """
    Unit test for Model.Rules.modus_tollendo_ponens.ModusTollendoPonens class
    """

    def test_modus_tollendo_ponens(self) -> None:
        """
        Testing rule function
        """
        self.assertEqual(ModusTollendoPonens.rule(ModusTollendoPonens(), '(A >> B)', 'C'), (False, ''))
        self.assertEqual(ModusTollendoPonens.rule(ModusTollendoPonens(), '(A >> B)', ''), (False, ''))
        self.assertEqual(ModusTollendoPonens.rule(ModusTollendoPonens(), '', ''), (False, ''))
        self.assertEqual(ModusTollendoPonens.rule(ModusTollendoPonens(), '(A >> B)', '~(A >> B)'), (False, ''))
        self.assertEqual(ModusTollendoPonens.rule(ModusTollendoPonens(), '(A | B)', '(A >> A >> B)'), (False, ''))

        self.assertEqual(ModusTollendoPonens.rule(ModusTollendoPonens(), '(A | B)', '~A'), (True, 'B'))
        self.assertEqual(ModusTollendoPonens.rule(ModusTollendoPonens(), '((B >> C) | (A >> (B >> C)))', '~(B >> C)'),
                         (True, '(A>>(B>>C))'))
        self.assertEqual(ModusTollendoPonens.rule(ModusTollendoPonens(), '((A >> (B >> C)) | ((A >> B) >> (A >> C)))',
                                                  '~(A >> (B >> C))'),
                         (True, '((A>>B)>>(A>>C))'))


if __name__ == "__main__":
    unittest.main()
