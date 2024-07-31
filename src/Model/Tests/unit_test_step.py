import unittest
from Model.step import Step
from Model.actions import Actions


class UnitTestStep(unittest.TestCase):

    def test_init(self) -> None:
        """
        Testing Step __init__ method, successful init and raising ValueError
        """
        step_one = Step(0, '(A >> B)', Actions.HYP)
        self.assertTrue(step_one.step_id == 0)
        self.assertTrue(step_one.formula == '(A >> B)')
        self.assertTrue(step_one.action == Actions.HYP)
        self.assertTrue(step_one.axiom_details == '')

        step_two = Step(1, '(A | B)', Actions.MP, '', 0, 1)
        self.assertTrue(step_two.step_id == 1)
        self.assertTrue(step_two.formula == '(A | B)')
        self.assertTrue(step_two.action == Actions.MP)
        self.assertTrue(step_two.rule_implication == 0)
        self.assertTrue(step_two.action == Actions.MP)
        self.assertTrue(step_two.axiom_details == '')

        step_three = Step(2, '~B', Actions.AXIOM)
        self.assertTrue(step_three.step_id == 2)
        self.assertTrue(step_three.formula == '~B')
        self.assertTrue(step_three.action == Actions.AXIOM)
        self.assertTrue(step_three.axiom_details == '')

        step_four = Step(1, '(A | B)', Actions.MT, '', 0, 1)
        self.assertTrue(step_four.step_id == 1)
        self.assertTrue(step_four.formula == '(A | B)')
        self.assertTrue(step_four.axiom_details == '')
        self.assertTrue(step_four.action == Actions.MT)

        step_five = Step(1, '(A | B)', Actions.MTP, '', 0, 1)
        self.assertTrue(step_five.step_id == 1)
        self.assertTrue(step_five.formula == '(A | B)')
        self.assertTrue(step_five.axiom_details == '')
        self.assertTrue(step_five.action == Actions.MTP)

        with self.assertRaises(ValueError):
            Step(3, 'A | | B', Actions.HYP)
            Step(-1, 'A', Actions.HYP)
            Step(1, 'A', Actions.HYP, '', 0, 1)
            Step(1, 'A', Actions.MTP, '', 1, 1)
            Step(4, 'A', 'Actions.HYP')


if __name__ == "__main__":
    unittest.main()
