import os.path
import unittest
from Model.model import Model
from Model.step import Step
from Model.actions import Actions


class UnitTestModel(unittest.TestCase):
    """
    Unit tests for Model.model.py functions.
    """

    def test_init(self) -> None:
        """
        Unit test for Model.model.__init__ function
        """
        model = Model(formula_set=['(A >> B)', '(B >> C)'], consequence_formula='(A >> C)')
        self.assertEqual(model.formula_set, ['(A >> B)', '(B >> C)'])
        self.assertEqual(model.consequence_formula, '(A >> C)')
        self.assertEqual(len(model.steps), 0)
        self.assertEqual(model.number_of_steps, 0)
        self.assertEqual(model.end, False)
        self.assertIn("(A >> (B >> A))", model.base_axioms)
        self.assertIn("(A >> A)", model.base_axioms)
        self.assertIn("(B >> (A | B))", model.base_axioms)

        with self.assertRaises(ValueError):
            Model(['A << B'], 'A')
            Model(['A >> B'], 'A << B')
            Model(['A >> B'], 'a')

    def test_new(self) -> None:
        """
        Unit test for Model.model.new function
        """
        model = Model(['(B >> C)', '(A >> C)'], '(A >> B)')
        model.new(['(A >> B)', '(B >> C)'], '(A >> C)')
        self.assertEqual(model.formula_set, ['(A >> B)', '(B >> C)'])
        self.assertEqual(model.consequence_formula, '(A >> C)')
        self.assertEqual(len(model.steps), 0)
        self.assertEqual(model.number_of_steps, 0)
        self.assertEqual(model.end, False)
        self.assertIn("(A >> (B >> A))", model.base_axioms)
        self.assertIn("(A >> A)", model.base_axioms)
        self.assertIn("(B >> (A | B))", model.base_axioms)

        with self.assertRaises(ValueError):
            model.new(['A << B'], 'A')
            model.new(['A >> B'], 'A << B')
            model.new(['A >> B'], 'a')

    def test__Model__input_checker(self) -> None:
        """
        Unit test for Model.model._Model__input_checker function
        """
        formula_set_0 = ['(A >> B)', '(B >> C)']
        consequence_formula_0 = '(A >> C)'
        formula_set_1 = []
        consequence_formula_1 = '(A >> C)'
        formula_set_2 = ['(A >> B)', '(B >> C)', '(B >> C)', '(A | B)']
        consequence_formula_2 = '(A >> C)'
        try:
            model = Model(formula_set_0, consequence_formula_0)
            model._Model__input_checker(formula_set_0, consequence_formula_0)
            model = Model(formula_set_1, consequence_formula_1)
            model._Model__input_checker(formula_set_1, consequence_formula_1)
            model = Model(formula_set_2, consequence_formula_2)
            model._Model__input_checker(formula_set_2, consequence_formula_2)
        except ValueError:
            self.fail()

        formula_set_0 = ['']
        consequence_formula_0 = '(A >> C)'
        formula_set_1 = ['(A >> B)', '(B >> C)']
        consequence_formula_1 = ''
        formula_set_2 = ['(A >> B)', '(B >> C)', '(B || C)', '(A | B)']
        consequence_formula_2 = '(A >> C)'

        with self.assertRaises(ValueError):
            model = Model(formula_set_0, consequence_formula_0)
            model._Model_Model__input_checker(formula_set_0, consequence_formula_0)
            model = Model(formula_set_1, consequence_formula_1)
            model._Model__input_checker(formula_set_1, consequence_formula_1)
            model = Model(formula_set_2, consequence_formula_2)
            model._Model__input_checker(formula_set_2, consequence_formula_2)

    def test__Model__axiom_checker(self) -> None:
        """
        Unit test for Model.model._Model__axiom_checker function
        """
        formula_list = ['(A >> (B >> A))', '((A >> (B >> C)) >> ((A >> B) >> (A >> C)))',
                        '((~A >> B) >> ((~A >> ~B) >> A))', '(A >> A)', '((A >> B) >> ((B >> C) >> (A >> C)))',
                        '(A >> (~~A))', '((~~A) >> A)', '((A >> B) >> (~~A >> ~~B))', '(A >> (B >> (A & B)))',
                        '((A & B) >> A)', '((A & B) >> B)', '(B >> (A | B))', '(A >> (A | B))',
                        '((A >> C) >> ((B >> C) >> (A | B >> C)))']
        self.assertTrue(Model._Model__axiom_checker(formula_list))
        formula_list = ['(A | B)', '(A >> B)']
        self.assertFalse(Model._Model__axiom_checker(formula_list))

    def test_action_hyp(self) -> None:
        """
        Unit test for Model.model.action_hyp function
        """
        model = Model(['(A >> B)', '(B >> C)'], '(A >> C)')
        step = Step(0, '(A >> B)', Actions.HYP)
        self.assertEqual(model._Model__action_hyp(step), step)
        step = Step(0, '(B >> C)', Actions.HYP)
        self.assertEqual(model._Model__action_hyp(step), step)
        step = Step(0, '(A >> C)', Actions.HYP)
        self.assertEqual(model._Model__action_hyp(step), None)
        step = Step(0, '(A >> C)', Actions.MP)
        self.assertEqual(model._Model__action_hyp(step), None)
        step = Step(0, '(A >> C)', Actions.AXIOM)
        self.assertEqual(model._Model__action_hyp(step), None)
        with self.assertRaises(ValueError):
            Step(-1, '(A >> C)', Actions.MP)

    def test__Model__action_axiom(self) -> None:
        """
        Unit test for Model.model.__action_axiom function
        """
        model = Model(['(A >> B)', '(B >> C)'], '(A >> C)')
        step = Step(0, '(A >> (B >> A))', Actions.AXIOM)
        data = ['A', 'B']
        model._Model__action_axiom(step, data)
        step = Step(0, '((A >> (B >> C)) >> ((A >> B) >> (A >> C)))', Actions.AXIOM)
        data = ['A', 'B', 'C']
        model._Model__action_axiom(step, data)
        self.assertEqual(step.formula, '((A >> (B >> C)) >> ((A >> B) >> (A >> C)))')
        step = Step(0, '(A >> (B >> A))', Actions.AXIOM)
        data = ['(C >> D)', '(D >> C)']
        model._Model__action_axiom(step, data)
        self.assertEqual(step.formula, '((C >> D) >> ((D >> C) >> (C >> D)))')
        step = Step(0, '(A >> (B >> A))', Actions.AXIOM)
        data = ['B', 'A']
        model._Model__action_axiom(step, data)
        self.assertEqual(step.formula, '(B >> (A >> B))')
        step = Step(0, '(A >> B)', Actions.AXIOM)
        data = ['(C >> D)', '(D >> C)']
        step = model._Model__action_axiom(step, data)
        self.assertEqual(step, None)
        step = Step(0, '(A | B)', Actions.AXIOM)
        data = ['(C >> D)', '(D >> C)']
        step = model._Model__action_axiom(step, data)
        self.assertEqual(step, None)
        step = Step(0, '(A | B)', Actions.AXIOM)
        data = []
        step = model._Model__action_axiom(step, data)
        self.assertEqual(step, None)
        step = Step(0, '(A >> C)', Actions.MP)
        self.assertEqual(model._Model__action_axiom(step, data), None)
        step = Step(0, '(A >> C)', Actions.MP)
        self.assertEqual(model._Model__action_axiom(step, data), None)

    def test_action_modus_ponens(self) -> None:
        """
        Testing model.__action_syntax_rule function, with MP action parameter
        Testing return value when:
            -every param is correct
            -index out of range
            -execute MP on the given logical formulas is impossible
            -steps list appending is correct or not
        """
        model = Model(['(A >> B)', '(B >> C)'], '(A >> C)')
        model.steps.append(Step(0, '((A >> (B >> C)) >> ((A >> B) >> (A >> C)))', Actions.AXIOM))
        model.steps.append(Step(1, '((B >> C) >> (A >> (B >> C)))', Actions.AXIOM))
        model.steps.append(Step(2, '(B >> C)', Actions.HYP))
        self.assertEqual(len(model.steps), 3)
        step = Step(3, '', Actions.MP)
        self.assertEqual(model._Model__action_syntax_rule(step, -1, 0), None)
        self.assertEqual(model._Model__action_syntax_rule(step, 0, -1), None)
        self.assertEqual(model._Model__action_syntax_rule(step, 0, 0), None)
        self.assertEqual(model._Model__action_syntax_rule(step, 500, 0), None)
        step = Step(3, '', Actions.HYP)
        self.assertEqual(model._Model__action_syntax_rule(step, 1, 0), None)
        step = Step(3, '', Actions.AXIOM)
        self.assertEqual(model._Model__action_syntax_rule(step, 1, 0), None)
        step = Step(3, '', Actions.MP)
        implication_formula_number = 1
        formula_to_be_detached_number = 2
        model._Model__action_syntax_rule(step, implication_formula_number, formula_to_be_detached_number)
        model.steps.append(step)
        self.assertEqual(step.formula, '(A >> (B >> C))')
        self.assertEqual(len(model.steps), 4)
        step = Step(4, '', Actions.MP)
        implication_formula_number = 0
        formula_to_be_detached_number = 3
        model._Model__action_syntax_rule(step, implication_formula_number, formula_to_be_detached_number)
        model.steps.append(step)
        self.assertEqual(step.formula, '((A >> B) >> (A >> C))')
        self.assertEqual(len(model.steps), 5)
        model.steps.append(Step(5, '(A >> B)', Actions.HYP))
        self.assertEqual(len(model.steps), 6)
        step = Step(6, '', Actions.MP)
        implication_formula_number = 4
        formula_to_be_detached_number = 5
        model._Model__action_syntax_rule(step, implication_formula_number, formula_to_be_detached_number)
        model.steps.append(step)
        self.assertEqual(step.formula, '(A >> C)')
        self.assertEqual(len(model.steps), 7)
        model._Model__check_end()
        self.assertTrue(model.end)
        step = Step(6, '', Actions.MP)
        implication_formula_number = 4
        formula_to_be_detached_number = 5
        step = model._Model__action_syntax_rule(step, implication_formula_number, formula_to_be_detached_number)
        model.steps.append(step)
        self.assertEqual(step, None)

    def test_action_modus_tollens(self) -> None:
        """
        Testing model.__action_syntax_rule function, with MT action parameter
        Testing return value when:
            -every param is correct
            -index out of range
            -execute MP on the given logical formulas is impossible
            -steps list appending is correct or not
        """
        model = Model(['((B >> C) >> (A >> (B >> C)))', '~(A >> (B >> C))'], '(B >> C)')
        model.steps.append(Step(0, '((B >> C) >> (A >> (B >> C)))', Actions.HYP))
        model.steps.append(Step(1, '~(A >> (B >> C))', Actions.HYP))
        self.assertEqual(len(model.steps), 2)
        step = Step(2, '', Actions.MT)
        self.assertEqual(model._Model__action_syntax_rule(step, -1, 0), None)
        step = Step(2, '', Actions.MT)
        self.assertEqual(model._Model__action_syntax_rule(step, 0, -1), None)
        step = Step(2, '', Actions.MT)
        self.assertEqual(model._Model__action_syntax_rule(step, 0, 0), None)
        step = Step(2, '', Actions.MT)
        self.assertEqual(model._Model__action_syntax_rule(step, 500, 0), None)
        step = Step(2, '', Actions.MT)
        implication_formula_number = 0
        formula_to_be_detached_number = 1
        model._Model__action_syntax_rule(step, implication_formula_number, formula_to_be_detached_number)
        model.steps.append(step)
        self.assertEqual(step.formula, '~(B >> C)')
        self.assertEqual(len(model.steps), 3)

    def test_action_modus_tollendo_ponens(self) -> None:
        """
        Testing model.action_syntax_rule function, with MTP action parameter
        Testing return value when:
            -every param is correct
            -index out of range
            -execute MP on the given logical formulas is impossible
            -steps list appending is correct or not
        """
        model = Model(['((B >> C) | (A >> (B >> C)))', '~(B >> C)'], '(A >> (B >> C))')
        model.steps.append(Step(0, '((B >> C) | (A >> (B >> C)))', Actions.HYP))
        model.steps.append(Step(1, '~(B >> C)', Actions.HYP))
        self.assertEqual(len(model.steps), 2)
        step = Step(2, '', Actions.MTP)
        self.assertEqual(model._Model__action_syntax_rule(step, -1, 0), None)
        step = Step(2, '', Actions.MTP)
        self.assertEqual(model._Model__action_syntax_rule(step, 0, -1), None)
        step = Step(2, '', Actions.MTP)
        self.assertEqual(model._Model__action_syntax_rule(step, 0, 0), None)
        step = Step(2, '', Actions.MTP)
        self.assertEqual(model._Model__action_syntax_rule(step, 500, 0), None)
        step = Step(2, '', Actions.MTP)
        implication_formula_number = 0
        formula_to_be_detached_number = 1
        model._Model__action_syntax_rule(step, implication_formula_number, formula_to_be_detached_number)
        model.steps.append(step)
        self.assertEqual(step.formula, '(A >> (B >> C))')
        self.assertEqual(len(model.steps), 3)

    def test_action_modus_ponendo_tollens(self) -> None:
        """
        Testing model.__action_syntax_rule function, with MPT action parameter
        Testing return value when:
            -every param is correct
            -index out of range
            -execute MP on the given logical formulas is impossible
            -steps list appending is correct or not
        """
        model = Model(['(~(B >> C) >> ~(A >> (B >> C)))', '(A >> (B >> C))'], '(B >> C)')
        model.steps.append(Step(0, '(~(B >> C) >> ~(A >> (B >> C)))', Actions.HYP))
        model.steps.append(Step(1, '(A >> (B >> C))', Actions.HYP))
        self.assertEqual(len(model.steps), 2)
        step = Step(2, '', Actions.MPT)
        self.assertEqual(model._Model__action_syntax_rule(step, -1, 0), None)
        step = Step(2, '', Actions.MPT)
        self.assertEqual(model._Model__action_syntax_rule(step, 0, -1), None)
        step = Step(2, '', Actions.MPT)
        self.assertEqual(model._Model__action_syntax_rule(step, 0, 0), None)
        step = Step(2, '', Actions.MPT)
        self.assertEqual(model._Model__action_syntax_rule(step, 500, 0), None)
        step = Step(2, '', Actions.MPT)
        implication_formula_number = 0
        formula_to_be_detached_number = 1
        model._Model__action_syntax_rule(step, implication_formula_number, formula_to_be_detached_number)
        model.steps.append(step)
        self.assertEqual(step.formula, '(B >> C)')
        self.assertEqual(len(model.steps), 3)

    def test_action_conditional_syllogism(self) -> None:
        """
        Testing model.__action_syntax_rule function, with CS action parameter
        Testing return value when:
            -every param is correct
            -index out of range
            -execute MP on the given logical formulas is impossible
            -steps list appending is correct or not
        """
        model = Model(['((B >> C) >> ~(A >> (B >> C)))', '(~(A >> (B >> C)) >> ~~C)'], '((B >> C) >> ~~C)')
        model.steps.append(Step(0, '((B >> C) >> ~(A >> (B >> C)))', Actions.HYP))
        model.steps.append(Step(1, '(~(A >> (B >> C)) >> ~~C)', Actions.HYP))
        self.assertEqual(len(model.steps), 2)
        step = Step(2, '', Actions.CS)
        self.assertEqual(model._Model__action_syntax_rule(step, -1, 0), None)
        step = Step(2, '', Actions.CS)
        self.assertEqual(model._Model__action_syntax_rule(step, 0, -1), None)
        step = Step(2, '', Actions.CS)
        self.assertEqual(model._Model__action_syntax_rule(step, 0, 0), None)
        step = Step(2, '', Actions.CS)
        self.assertEqual(model._Model__action_syntax_rule(step, 500, 0), None)
        step = Step(2, '', Actions.CS)
        implication_formula_number = 0
        formula_to_be_detached_number = 1
        model._Model__action_syntax_rule(step, implication_formula_number, formula_to_be_detached_number)
        model.steps.append(step)
        self.assertEqual(step.formula, '((B >> C) >> ~~C)')
        self.assertEqual(len(model.steps), 3)

    def test_end(self) -> None:
        """
        Unit test for Model.model.end function
        """
        model = Model(['(A >> B)', '(B >> C)'], '(A >> C)')
        model._Model__check_end()
        self.assertFalse(model.end)
        model.steps.append(Step(0, '((A >> (B >> C)) >> ((A >> B) >> (A >> C)))', Actions.AXIOM))
        model._Model__check_end()
        self.assertFalse(model.end)
        model.steps.append(Step(1, '((B >> C) >> (A >> (B >> C)))', Actions.AXIOM))
        model._Model__check_end()
        self.assertFalse(model.end)
        model.steps.append(Step(2, '(B >> C)', Actions.HYP))
        model._Model__check_end()
        self.assertFalse(model.end)
        model.steps.append(Step(3, '(A >> C)', Actions.AXIOM))
        model._Model__check_end()
        self.assertTrue(model.end)

        model = Model(['(A >> C)', '(B >> C)'], '(A >> C)')
        model._Model__check_end()
        self.assertTrue(model.end)

    def test_steps_append(self) -> None:
        """
        Unit test for Model.model.__steps_append function
        """
        model = Model(['(A >> B)', '(B >> C)'], '(A >> C)')
        self.assertTrue(
            model._Model__steps_append(Step(0, '((A >> (B >> C)) >> ((A >> B) >> (A >> C)))', Actions.AXIOM)))
        self.assertTrue(model._Model__steps_append(Step(1, '((B >> C) >> (A >> (B >> C)))', Actions.AXIOM)))
        self.assertTrue(model._Model__steps_append(Step(2, '(B >> C)', Actions.HYP)))
        step = Step(3, '', Actions.MP)
        implication_formula_number = 1
        formula_to_be_detached_number = 2
        step = model._Model__action_modus_ponens(step, implication_formula_number, formula_to_be_detached_number)
        self.assertTrue(model._Model__steps_append(step))

        self.assertFalse(None)
        self.assertFalse(model._Model__steps_append(Step(2, '(B >> C)', Actions.HYP)))

    def test_get_formula_set_consequence_concat(self) -> None:
        """
        Unit test for Model.model.get_formula_set_consequence_concat function
        """
        model = Model(['A', 'B', '(A >> B)'], '~A')
        concat = '{A, B, (A >> B)} |- ~A'
        self.assertEqual(model.get_formula_set_consequence_concat(), concat)
        model = Model(['(C & D)', '(A | B)', '(A >> B)'], '((A | B) | C)')
        concat = '{(C & D), (A | B), (A >> B)} |- ((A | B) | C)'
        self.assertEqual(model.get_formula_set_consequence_concat(), concat)
        model = Model([], '(A >> (B >> A))')
        concat = '{ } |- (A >> (B >> A))'
        self.assertEqual(model.get_formula_set_consequence_concat(), concat)

    def test_get_steps_string(self) -> None:
        """
        Unit test for Model.model.get_steps_string function
        """
        model = Model(['(A >> B)', 'A'], 'B')
        self.assertTrue(model.add_step('(A >> B)', Actions.HYP))
        self.assertTrue(model.add_step('A', Actions.HYP))
        self.assertTrue(model.add_step('(A >> (B >> A))', Actions.AXIOM, data=['A', 'B']))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=2, formula_to_be_detached_number=1))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=0, formula_to_be_detached_number=1))
        steps = model.get_steps_string()
        self.assertEqual(len(steps), 5)
        self.assertEqual(steps[0], '1. (A >> B) [HYP]')
        self.assertEqual(steps[1], '2. A [HYP]')
        self.assertEqual(steps[2], '3. (A >> (B >> A)) [AXIOM: 1. A=A B=B]')
        self.assertEqual(steps[3], '4. (B >> A) [MP(3,2)]')
        self.assertEqual(steps[4], '5. B [MP(1,2)]')

    def test_get_hint(self) -> None:
        """
        Unit test for Model.model.get_hint function
        """
        model = Model(['(A >> B)', 'A'], 'B')
        self.assertTrue(model.add_step('(A >> B)', Actions.HYP))
        self.assertTrue(model.add_step('A', Actions.HYP))
        self.assertTrue(model.add_step('(A >> (B >> A))', Actions.AXIOM, data=['A', 'B']))
        self.assertEqual(model.get_hint(), (True, '(A >> B)', 'A'))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=0, formula_to_be_detached_number=1))
        self.assertEqual(model.get_hint(), (False, '', ''))

        model = Model(['(A >> B)', 'A'], 'B')
        self.assertTrue(model.add_step('A', Actions.HYP))
        self.assertTrue(model.add_step('(A >> (B >> A))', Actions.AXIOM, data=['A', 'B']))
        self.assertEqual(model.get_hint(), (True, '(A >> (B >> A))', 'A'))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=1, formula_to_be_detached_number=0))
        self.assertTrue(model.add_step('(A >> B)', Actions.HYP))
        self.assertEqual(model.get_hint(), (True, '(B >> A)', '(A >> (B >> A))'))
        pass

    def test_delete_steps(self) -> None:
        """
        Unit test for Model.model.delete_steps function
        """
        model = Model(['(A >> B)', 'A'], 'B')
        self.assertTrue(model.add_step('(A >> B)', Actions.HYP))
        self.assertTrue(model.add_step('A', Actions.HYP))
        self.assertTrue(model.add_step('(A >> (B >> A))', Actions.AXIOM, data=['A', 'B']))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=2, formula_to_be_detached_number=1))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=0, formula_to_be_detached_number=1))
        self.assertTrue(model.end)

        self.assertFalse(model.delete_steps(-1))

        self.assertTrue(model.delete_steps(2))
        self.assertEqual(len(model.steps), 2)
        self.assertTrue(model.steps[0].step_id == 0)
        self.assertTrue(model.steps[0].formula == '(A >> B)')
        self.assertTrue(model.steps[0].action == Actions.HYP)
        self.assertTrue(model.steps[1].step_id == 1)
        self.assertTrue(model.steps[1].formula == 'A')
        self.assertTrue(model.steps[1].action == Actions.HYP)

    def test_add_axiom(self) -> None:
        """
        Unit test for Model.model.add_axiom function
        """
        model = Model(['(A >> B)', 'A'], 'B')
        self.assertTrue(model.add_axiom('(A >> (~A >> B))'))
        self.assertEqual(model.added_axioms, ['(A >> (~A >> B))'])
        self.assertEqual(len(model.added_axioms), 1)

        self.assertFalse(model.add_axiom('(A >> (~A >> B))'))
        self.assertFalse(model.add_axiom('(A >> ~A)'))
        self.assertFalse(model.add_axiom('A'))
        self.assertFalse(model.add_axiom('(A | B)'))
        self.assertFalse(model.add_axiom('(A >> B)'))
        self.assertFalse(model.add_axiom('(A & B)'))
        self.assertFalse(model.add_axiom('(A v B)'))

    def test_action_added_axiom(self) -> None:
        """
        Unit test for Model.model.action_added_axiom function
        """
        model = Model(['~B', 'B'], 'A')
        self.assertTrue(model.add_axiom('(A >> (~A >> B))'))
        self.assertEqual(model.added_axioms, ['(A >> (~A >> B))'])
        self.assertEqual(len(model.added_axioms), 1)
        self.assertTrue(model.action_added_axiom('(A >> (~A >> B))', ['B', 'A']))
        self.assertEqual(model.steps[0].formula, '(B >> (~B >> A))')
        self.assertEqual(model.steps[0].action, Actions.AXIOM)

        self.assertFalse(model.action_added_axiom('(A >> ~A)', ['A']))
        self.assertFalse(model.action_added_axiom('(A >> A)', ['A']))
        self.assertFalse(model.action_added_axiom('(A | A)', ['A']))

    def test_formula_set_contains_tautology(self) -> None:
        """
        Unit test for Model.model.formula_set_contains_tautology function
        """
        formula_set = ['A', 'B', '(A | ~A)']
        consequence_formula = 'C'
        model = Model(formula_set, consequence_formula)
        self.assertTrue(model.formula_set_contains_tautology())
        formula_set = ['A', 'B', '(A | ~A)', '(A >> A)']
        consequence_formula = 'C'
        model = Model(formula_set, consequence_formula)
        self.assertTrue(model.formula_set_contains_tautology())
        formula_set = ['A', 'B']
        consequence_formula = 'C'
        model = Model(formula_set, consequence_formula)
        self.assertFalse(model.formula_set_contains_tautology())

    def test_delete_tautologies(self) -> None:
        """
        Unit test for Model.model.delete_tautologies function
        """
        formula_set = ['A', 'B', '(A | ~A)']
        consequence_formula = 'C'
        model = Model(formula_set, consequence_formula)
        self.assertTrue(model.delete_tautologies())
        self.assertEqual(model.formula_set, ['A', 'B'])
        formula_set = ['A', 'B', '(A | ~A)', '(A >> A)']
        consequence_formula = 'C'
        model = Model(formula_set, consequence_formula)
        self.assertTrue(model.delete_tautologies())
        self.assertEqual(model.formula_set, ['A', 'B'])
        formula_set = ['A', 'B']
        consequence_formula = 'C'
        model = Model(formula_set, consequence_formula)
        self.assertFalse(model.delete_tautologies())
        self.assertEqual(model.formula_set, ['A', 'B'])

    def test_task_is_provable(self) -> None:
        """
        Unit test for Model.model.task_is_provable function
        """
        model = Model(['(A >> B)', 'A'], 'B')
        self.assertTrue(model.task_is_provable())
        model = Model(['((B >> C) >> (A >> (B >> C)))', '~(A >> (B >> C))'], '~(B >> C)')
        self.assertTrue(model.task_is_provable())
        model = Model(['~B', 'B'], 'A')
        self.assertTrue(model.task_is_provable())
        model = Model(['(A >> B)', '~B'], '~A')
        self.assertTrue(model.task_is_provable())
        model = Model(['(A >> B)', '~B'], '~A')
        self.assertTrue(model.task_is_provable())
        model = Model(['(F >> K)', '(K >> A)', '~A'], '~F')
        self.assertTrue(model.task_is_provable())
        model = Model(['(A >> B)', '(B >> C)'], '(A >> C)')
        self.assertTrue(model.task_is_provable())
        model = Model(['(A & B)'], 'B')
        self.assertTrue(model.task_is_provable())
        model = Model(['A', 'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'W', 'R', 'T', 'Z', 'U'], 'A')
        self.assertTrue(model.task_is_provable())

        model = Model(['(A >> B)'], 'B')
        self.assertFalse(model.task_is_provable())
        model = Model(['(A | B)'], 'B')
        self.assertFalse(model.task_is_provable())
        model = Model(['(A >> B)'], '~A')
        self.assertFalse(model.task_is_provable())
        model = Model(['(F >> K)', '~A'], '~F')
        self.assertFalse(model.task_is_provable())
        model = Model(['((B >> C) >> (A >> (B >> C)))'], '~(B >> C)')
        self.assertFalse(model.task_is_provable())

    def test_save_model(self) -> None:
        """
        Unit test for Model.model.save_model function
        """
        import json
        from datetime import datetime
        from Persistence.data_access import DataAccess
        model = Model(['(A >> B)', 'A'], 'B')
        self.assertTrue(model.add_step('(A >> B)', Actions.HYP))
        self.assertTrue(model.add_step('A', Actions.HYP))
        self.assertTrue(model.add_step('(A >> (B >> A))', Actions.AXIOM, data=['A', 'B']))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=2, formula_to_be_detached_number=1))
        self.assertTrue(model.add_step('', Actions.MP, implication_formula_number=0, formula_to_be_detached_number=1))
        self.assertTrue(model.add_axiom('(A >> (~A >> B))'))
        self.assertTrue(model.save_model())
        now = datetime.now()
        file = now.strftime("%Y-%m-%d_%H-%M") + '.json'
        data_access = DataAccess()
        path = data_access._DataAccess__get_saves_persistence_path()
        path = os.path.join(path, file)
        with open(path) as f:
            data = json.load(f)
            f.close()
        self.assertEqual(data['formula_set'], ['(A >> B)', 'A'])
        self.assertEqual(data['consequence_formula'], 'B')
        self.assertEqual(data['end'], True)
        self.assertEqual(data['number_of_steps'], 5)
        steps = [
            [0, '(A >> B)', 'Actions.HYP', '', 0, 0],
            [1, 'A', 'Actions.HYP', '', 0, 0],
            [2, '(A >> (B >> A))', 'Actions.AXIOM', '[AXIOM: 1. A=A B=B]', 0, 0],
            [3, '(B >> A)', 'Actions.MP', '', 2, 1],
            [4, 'B', 'Actions.MP', '', 0, 1]
        ]
        self.assertEqual(data['steps'], steps)
        self.assertEqual(data['task_name'], '{(A >> B), A} |- B')
        self.assertEqual(data['added_axioms'], ['(A >> (~A >> B))'])

    def test_load_model(self) -> None:
        """
        Unit test for Model.model.load_model function
        """
        import json
        from Persistence.data_access import DataAccess
        data = {
            "formula_set": ["(A >> B)", "A"],
            "consequence_formula": "B",
            "end": True,
            "number_of_steps": 5,
            "steps": [
                [0, "(A >> B)", "Actions.HYP", '', 0, 0],
                [1, "A", "Actions.HYP", '', 0, 0],
                [2, "(A >> (B >> A))", "Actions.AXIOM", '', 0, 0],
                [3, "(B >> A)", "Actions.MP", '', 2, 1],
                [4, "B", "Actions.MP", '', 0, 1]
            ],
            "task_name": "{(A >> B), A} |- B",
            "added_axioms": ['(A >> (~A >> B))']
        }
        file = 'test.json'
        data_access = DataAccess()
        path = data_access._DataAccess__get_saves_persistence_path()
        path = os.path.join(path, file)
        with open(path, 'w') as f:
            json.dump(data, f)
            f.close()
        model = Model(formula_set=None, consequence_formula=None, file_path=path)
        self.assertEqual(model.formula_set, ["(A >> B)", "A"])
        self.assertEqual(model.consequence_formula, "B")
        self.assertTrue(model.end)
        self.assertEqual(model.number_of_steps, 5)
        self.assertEqual(model.steps[0].step_id, 0)
        self.assertEqual(model.steps[1].step_id, 1)
        self.assertEqual(model.steps[2].step_id, 2)
        self.assertEqual(model.steps[3].step_id, 3)
        self.assertEqual(model.steps[4].step_id, 4)
        self.assertEqual(model.steps[0].formula, "(A >> B)")
        self.assertEqual(model.steps[1].formula, "A")
        self.assertEqual(model.steps[2].formula, "(A >> (B >> A))")
        self.assertEqual(model.steps[3].formula, "(B >> A)")
        self.assertEqual(model.steps[4].formula, "B")
        self.assertEqual(model.steps[0].action, Actions.HYP)
        self.assertEqual(model.steps[1].action, Actions.HYP)
        self.assertEqual(model.steps[2].action, Actions.AXIOM)
        self.assertEqual(model.steps[3].action, Actions.MP)
        self.assertEqual(model.steps[4].action, Actions.MP)
        self.assertEqual(model.steps[3].rule_implication, 2)
        self.assertEqual(model.steps[3].rule_detached, 1)
        self.assertEqual(model.steps[4].rule_implication, 0)
        self.assertEqual(model.steps[4].rule_detached, 1)
        self.assertEqual(model.get_formula_set_consequence_concat(), "{(A >> B), A} |- B")
        self.assertEqual(model.added_axioms, ['(A >> (~A >> B))'])


if __name__ == "__main__":
    unittest.main()
