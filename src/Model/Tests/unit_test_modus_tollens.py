import unittest
from Model.Rules.modus_tollens import ModusTollens as MT


class UnitTestModusTollens(unittest.TestCase):
    """
    Unit test for Model.Rules.modus_tollens.ModusTollens class
    """

    def test_modus_tollens(self) -> None:
        """
        Testing rule function
        """
        self.assertEqual(MT.rule(MT(), '', ''), (False, ''))
        self.assertEqual(MT.rule(MT(), '', 'A'), (False, ''))
        self.assertEqual(MT.rule(MT(), 'A', ''), (False, ''))
        self.assertEqual(MT.rule(MT(), '(A >> B)', 'B'), (False, ''))
        self.assertEqual(MT.rule(MT(), '((B >> C) >> (A >> (B >> C)))', '(B >> C)'), (False, ''))
        self.assertEqual(MT.rule(MT(), '((A >> (B >> C)) >> ((A >> B) >> (A >> C)))', '(A >> (B >> C))'), (False, ''))

        self.assertEqual(MT.rule(MT(), '(A >> B)', '~B'), (True, '~A'))
        self.assertEqual(MT.rule(MT(), '((B >> C) >> (A >> (B >> C)))', '~(A >> (B >> C))'), (True, '~(B>>C)'))
        self.assertEqual(MT.rule(MT(), '((A >> (B >> C)) >> ((A >> B) >> (A >> C)))', '~((A >> B) >> (A >> C))'),
                         (True, '~(A>>(B>>C))'))


if __name__ == "__main__":
    unittest.main()
