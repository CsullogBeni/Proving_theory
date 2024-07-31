import unittest
from Model.model import Model
from Model.actions import Actions
from Model.formula_in_steps_exception import FormulaInStepsException


class SystemTestModel(unittest.TestCase):
    """
    System testing Model.model.py
    """

    def test_task_0(self) -> None:
        """
        Trying to prove transitivity
        Task:
        {A ⊃ B, B ⊃ C} |- A ⊃ C
        """
        try:
            model = Model(['(A >> B)', '(B >> C)'], '(A >> C)')
        except ValueError:
            self.fail()
        self.assertNotEqual(model, None)
        self.assertTrue(
            model.add_step('((A >> (B >> C)) >> ((A >> B) >> (A >> C)))', Actions.AXIOM, data=['A', 'B', 'C']))
        self.assertTrue(model.add_step('(A >> (B >> A))', Actions.AXIOM, data=['(B >> C)', 'A']))
        self.assertTrue(model.add_step('(B >> C)', Actions.HYP))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=1, formula_to_be_detached_number=2))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=0, formula_to_be_detached_number=3))
        self.assertTrue(model.add_step('(A >> B)', Actions.HYP))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=4, formula_to_be_detached_number=5))
        self.assertEqual((model.steps[len(model.steps) - 1]).formula, '(A >> C)')
        self.assertTrue(model.end)
        self.assertEqual(len(model.steps), 7)
        self.assertEqual(model.number_of_steps, 7)

    def test_task_1(self) -> None:
        """
        Trying to prove:
        {F ⊃ K, K ⊃ A, ¬A} |- ¬F
        """
        try:
            model = Model(['(F >> K)', '(K >> A)', '~A'], '~F')
        except ValueError:
            self.fail()
        self.assertNotEqual(model, None)
        self.assertTrue(model.add_step('((~A >> B) >> ((~A >> ~B) >> A))', Actions.AXIOM, data=['~F', '~A']))
        self.assertTrue(model.add_step('(A >> (B >> A))', Actions.AXIOM, data=['~A', '~~F']))
        self.assertTrue(model.add_step('~A', Actions.HYP))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=1, formula_to_be_detached_number=2))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=0, formula_to_be_detached_number=3))
        self.assertTrue(model.add_step('((A >> B) >> (~~A >> ~~B))', Actions.AXIOM, data=['F', 'A']))
        self.assertTrue(
            model.add_step('((A >> (B >> C)) >> ((A >> B) >> (A >> C)))', Actions.AXIOM, data=['F', 'K', 'A']))
        self.assertTrue(model.add_step('(A >> (B >> A))', Actions.AXIOM, data=['(K >> A)', 'F']))
        self.assertTrue(model.add_step('(K >> A)', Actions.HYP))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=7, formula_to_be_detached_number=8))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=6, formula_to_be_detached_number=9))
        self.assertTrue(model.add_step('(F >> K)', Actions.HYP))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=10, formula_to_be_detached_number=11))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=5, formula_to_be_detached_number=12))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=4, formula_to_be_detached_number=13))
        self.assertEqual((model.steps[len(model.steps) - 1]).formula, '~F')
        self.assertTrue(model.end)
        self.assertEqual(len(model.steps), 15)
        self.assertEqual(model.number_of_steps, 15)

    def test_task_2(self) -> None:
        """
        Trying to prove:
         {A ⊃ B , ¬B } |- ¬A
        """
        try:
            model = Model(['(A >> B)', '~B'], '~A')
        except ValueError:
            self.fail()
        self.assertNotEqual(model, None)
        self.assertTrue(model.add_step('((~A >> B) >> ((~A >> ~B) >> A))', Actions.AXIOM, data=['~A', '~B']))
        self.assertTrue(model.add_step('(A >> (B >> A))', Actions.AXIOM, data=['~B', '~~A']))
        self.assertTrue(model.add_step('~B', Actions.HYP))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=1, formula_to_be_detached_number=2))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=0, formula_to_be_detached_number=3))
        self.assertTrue(model.add_step('((A >> B) >> (~~A >> ~~B))', Actions.AXIOM, data=['A', 'B']))
        self.assertTrue(model.add_step('(A >> B)', Actions.HYP))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=5, formula_to_be_detached_number=6))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=4, formula_to_be_detached_number=7))
        self.assertEqual((model.steps[len(model.steps) - 1]).formula, '~A')
        self.assertTrue(model.end)
        self.assertEqual(len(model.steps), 9)
        self.assertEqual(model.number_of_steps, 9)

    def test_edge_cases_1(self) -> None:
        """
        Trying to prove:
         {A ⊃ B , ¬B } |- ¬A
        """
        try:
            model = Model(['(A >> B)', '~B'], '~A')
        except ValueError:
            self.fail()
        self.assertNotEqual(model, None)
        self.assertTrue(model.add_step('((~A >> B) >> ((~A >> ~B) >> A))', Actions.AXIOM, data=['~A', '~B']))
        self.assertTrue(model.add_step('(A >> (B >> A))', Actions.AXIOM, data=['~B', '~~A']))
        self.assertTrue(model.add_step('~B', Actions.HYP))
        self.assertFalse(model.add_step('((~A >> B) | ((~A >> ~B) >> A))', Actions.AXIOM, data=['~A', '~B']))
        with self.assertRaises(FormulaInStepsException):
            self.assertFalse(model.add_step('~B', Actions.HYP))
        self.assertEqual((model.steps[len(model.steps) - 1]).formula, '~B')

        self.assertFalse(model.end)
        self.assertEqual(len(model.steps), 3)
        self.assertEqual(model.number_of_steps, 3)
        self.assertFalse(model.add_step('', Actions.MP, implication_formula_number=2, formula_to_be_detached_number=1))
        self.assertFalse(model.add_step('', Actions.MP, implication_formula_number=0, formula_to_be_detached_number=1))
        self.assertFalse(model.add_step('', Actions.MP, implication_formula_number=0, formula_to_be_detached_number=2))
        self.assertEqual((model.steps[len(model.steps) - 1]).formula, '~B')
        self.assertFalse(model.end)
        self.assertEqual(len(model.steps), 3)
        self.assertEqual(model.number_of_steps, 3)
        self.assertFalse(model.add_step('(A >> (B >> A))', Actions.AXIOM, data=['~B', '~~A', 'Z']))
        self.assertFalse(model.add_step('(A >> (B >> A))', Actions.AXIOM, data=['~B', '|']))
        self.assertEqual((model.steps[len(model.steps) - 1]).formula, '~B')
        self.assertFalse(model.end)
        self.assertEqual(len(model.steps), 3)
        self.assertEqual(model.number_of_steps, 3)

    def test_edge_cases_2(self) -> None:
        """
        Trying to prove:
         {A ⊃ B , A } |- B
        """
        try:
            model = Model(['(A >> B)', 'A'], 'B')
        except ValueError:
            self.fail()
        self.assertNotEqual(model, None)
        self.assertTrue(model.add_step('A', Actions.HYP))
        with self.assertRaises(FormulaInStepsException):
            self.assertFalse(model.add_step('A', Actions.HYP))
        self.assertTrue(model.add_step('(A >> B)', Actions.HYP))
        with self.assertRaises(FormulaInStepsException):
            self.assertFalse(model.add_step('(A >> B)', Actions.HYP))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=1, formula_to_be_detached_number=0))
        self.assertEqual((model.steps[len(model.steps) - 1]).formula, 'B')
        self.assertTrue(model.end)
        self.assertEqual(len(model.steps), 3)
        self.assertEqual(model.number_of_steps, 3)

    def test_proving_with_added_axiom(self) -> None:
        """
        Adding to added_axioms: (A ⊃ (¬A ⊃ B))

        Trying to prove:
         { B, ¬B } |- A
        """
        model = Model(['~B', 'B'], 'A')
        self.assertTrue(model.add_axiom('(A >> (~A >> B))'))
        self.assertTrue(model.action_added_axiom('(A >> (~A >> B))', ['B', 'A']))
        self.assertTrue(model.add_step('B', Actions.HYP))
        self.assertTrue(model.add_step('~B', Actions.HYP))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=0, formula_to_be_detached_number=1))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=3, formula_to_be_detached_number=2))
        self.assertEqual((model.steps[len(model.steps) - 1]).formula, 'A')
        self.assertTrue(model.end)
        self.assertEqual(len(model.steps), 5)
        self.assertEqual(model.number_of_steps, 5)

    def test_proving_with_modus_tollens(self) -> None:
        """
        Trying to use Modus Tollens rule.

        Trying to prove:
         { ((B ⊃ C) ⊃ (A ⊃ (B ⊃ C))), ¬(A ⊃ (B ⊃ C))} |- ¬(B ⊃ C)
        """
        model = Model(['((B >> C) >> (A >> (B >> C)))', '~(A >> (B >> C))'], '~(B >> C)')
        self.assertTrue(model.add_step('((B >> C) >> (A >> (B >> C)))', Actions.HYP))
        self.assertTrue(model.add_step('~(A >> (B >> C))', Actions.HYP))
        self.assertEqual(len(model.steps), 2)
        self.assertFalse(model.end)
        self.assertTrue(model.add_step('', Actions.MT, implication_formula_number=0, formula_to_be_detached_number=1))
        self.assertEqual(len(model.steps), 3)
        self.assertEqual(model.number_of_steps, 3)
        self.assertTrue(model.end)

    def test_proving_with_delete_axioms(self) -> None:
        """
        Trying to use tautology deletions before proving.

        Trying to prove:
         { A, (A ⊃ B), (A ∨ ¬A), (A ⊃ A) } |- B
        """
        formula_set = ['A', '(A >> B)', '(A | ~A)', '(A >> A)']
        consequence_formula = 'B'
        model = Model(formula_set, consequence_formula)
        self.assertTrue(model.formula_set_contains_tautology())
        self.assertTrue(model.delete_tautologies())
        self.assertEqual(model.formula_set, ['A', '(A >> B)'])
        self.assertTrue(model.add_step('A', Actions.HYP))
        self.assertTrue(model.add_step('(A >> B)', Actions.HYP))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=1, formula_to_be_detached_number=0))
        self.assertEqual(len(model.steps), 3)
        self.assertEqual(model.number_of_steps, 3)
        self.assertTrue(model.end)

    def test_trying_modus_ponendo_tollens_rule(self) -> None:
        """
        Trying to use modus ponendo tollens rule.

        Trying to prove:
        {¬A ⊃ ¬B, B} |- A
         { ¬(A ⊃ (B ⊃ A)) ⊃ ¬((C ∧ D) ⊃ H), ((C ∧ D) ⊃ H) } |- (A ⊃ (B ⊃ A))
        """
        formula_set = ['(~(A >> (B >> A)) >> ~((C & D) >> H))', '((C & D) >> H)']
        consequence_formula = '(A >> (B >> A))'
        model = Model(formula_set, consequence_formula)
        self.assertIsNotNone(model)
        self.assertTrue(model.add_step('(~(A >> (B >> A)) >> ~((C & D) >> H))', Actions.HYP))
        self.assertTrue(model.add_step('((C & D) >> H)', Actions.HYP))
        self.assertTrue(model.add_step('', Actions.MPT, implication_formula_number=0, formula_to_be_detached_number=1))
        self.assertTrue(model.steps[2].formula == '(A >> (B >> A))')
        self.assertTrue(model.end)
        self.assertTrue(len(model.steps) == 3)

    def test_trying_modus_tollendo_ponens_rule(self) -> None:
        """
        Trying to use modus tollendo ponens rule.

        Trying to prove:
         { (A ⊃ (B ⊃ A)) | ((C ∧ D) ⊃ H), ¬(A ⊃ (B ⊃ A)) } |- ((C ∧ D) ⊃ H)
        """
        formula_set = ['((A >> (B >> A)) | ((C & D) >> H))', '~(A >> (B >> A))']
        consequence_formula = '((C & D) >> H)'
        model = Model(formula_set, consequence_formula)
        self.assertIsNotNone(model)
        self.assertTrue(model.add_step('((A >> (B >> A)) | ((C & D) >> H))', Actions.HYP))
        self.assertTrue(model.add_step('~(A >> (B >> A))', Actions.HYP))
        self.assertTrue(model.add_step('', Actions.MTP, implication_formula_number=0, formula_to_be_detached_number=1))
        self.assertTrue(model.steps[2].formula == '((C & D) >> H)')
        self.assertTrue(model.end)
        self.assertTrue(len(model.steps) == 3)

    def test_trying_conditional_syllogism_rule(self) -> None:
        """
        Trying to use conditional syllogism rule.

        Trying to prove:
         {((A ⊃ (B ⊃ A)) ⊃ ((A | C) ⊃ (B ⊃ C))), (((A | C) ⊃ (B ⊃ C)) ⊃ ¬((A | C) ∧ B)) }
         |- ((A ⊃ (B ⊃ A)) ⊃ ¬((A | C) ∧ B))
        """
        formula_set = ['((A >> (B >> A)) >> ((A | C) >> (B >> C)))', '(((A | C) >> (B >> C)) >> ~((A | C) & B))']
        consequence_formula = '((A >> (B >> A)) >> ~((A | C) & B))'
        model = Model(formula_set, consequence_formula)
        self.assertIsNotNone(model)
        self.assertTrue(model.add_step('((A >> (B >> A)) >> ((A | C) >> (B >> C)))', Actions.HYP))
        self.assertTrue(model.add_step('(((A | C) >> (B >> C)) >> ~((A | C) & B))', Actions.HYP))
        self.assertTrue(model.add_step('', Actions.CS, implication_formula_number=0, formula_to_be_detached_number=1))
        self.assertTrue(model.steps[2].formula == '((A >> (B >> A)) >> ~((A | C) & B))')
        self.assertTrue(model.end)
        self.assertTrue(len(model.steps) == 3)

    def test_consequence_in_formula_set(self):
        """
        Testing that the model recognized if the consequence formula in the formula set. Then the task is automatically
        proved.

        Trying to prove:
            { A } |- A
        """
        formula_set = ['A']
        consequence_formula = 'A'
        model = Model(formula_set, consequence_formula)
        self.assertTrue(model.end)
        self.assertTrue(len(model.steps) == 0)


if __name__ == '__main__':
    unittest.main()
