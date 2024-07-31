import unittest
from Model.Rules.conditional_syllogism import ConditionalSyllogism


class UnitTestModusTollendoPonens(unittest.TestCase):
    """
    Unit test for Model.Rules.modus_tollendo_ponens.ModusTollendoPonens class
    """

    def test_conditional_syllogism(self):
        """
        Testing rule function
        """
        self.assertEqual(ConditionalSyllogism.rule(ConditionalSyllogism(),'(A >> B)', 'C'), (False, ''))
        self.assertEqual(ConditionalSyllogism.rule(ConditionalSyllogism(),'(A >> B)', ''), (False, ''))
        self.assertEqual(ConditionalSyllogism.rule(ConditionalSyllogism(),'', ''), (False, ''))
        self.assertEqual(ConditionalSyllogism.rule(ConditionalSyllogism(),'(A >> B)', '~(A >> B)'), (False, ''))
        self.assertEqual(ConditionalSyllogism.rule(ConditionalSyllogism(),'(A | B)', '(A >> A >> B)'), (False, ''))

        self.assertEqual(ConditionalSyllogism.rule(ConditionalSyllogism(),'(A >> B)', '(B >> C)'), (True, '(A>>C)'))
        self.assertEqual(ConditionalSyllogism.rule(ConditionalSyllogism(),'(A >> ~B)', '(~B >> C)'), (True, '(A>>C)'))
        self.assertEqual(ConditionalSyllogism.rule(ConditionalSyllogism(),'((A | B) >> (B | C))', '((B | C) >> (C | D))'),
                         (True, '((A|B)>>(C|D))'))
        self.assertEqual(ConditionalSyllogism.rule(ConditionalSyllogism(),'((A | B) >> ~~(B | C))', '(~~(B | C) >> (C | D))'),
                         (True, '((A|B)>>(C|D))'))
        self.assertEqual(ConditionalSyllogism.rule(ConditionalSyllogism(),'((A >> (B >> C)) >> (C | D))', '((C | D) >> (A >> C))'),
                         (True, '((A>>(B>>C))>>(A>>C))'))
        self.assertEqual(ConditionalSyllogism.rule(ConditionalSyllogism(),'(A >> ~~(A >> (B >> A)))', '(~~(A >> (B >> A)) >> B)'),
                         (True, '(A>>B)'))


if __name__ == "__main__":
    unittest.main()
