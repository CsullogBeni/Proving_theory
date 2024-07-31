import unittest
from Model.model import Model
from Model.solver import Solver


class SystemTestSolver(unittest.TestCase):
    """
    System testing Model.solver.py
    """

    def test_task_0(self) -> None:
        """
        Trying to prove the task below.
        Task:
        {A ⊃ B, A} |- B
        """
        model = Model(['(A >> B)', 'A'], 'B')
        result = Solver.solve(model)
        successful = result[0]
        proving_theory_list = result[1]
        print(proving_theory_list)
        self.assertTrue(successful)
        self.assertIn('B', proving_theory_list[len(proving_theory_list)-1])

    def test_task_1(self) -> None:
        """
        Trying to prove transitivity
        Task:
        {A ⊃ B, B ⊃ C} |- A ⊃ C
        """
        model = Model(['(A >> B)', '(B >> C)'], '(A >> C)')
        result = Solver.solve(model)
        successful = result[0]
        proving_theory_list = result[1]
        print(proving_theory_list)
        self.assertTrue(successful)
        self.assertIn('(A >> C)', proving_theory_list[len(proving_theory_list)-1])

    def test_task_2(self) -> None:
        """
        Trying to prove the task below.
        Task:
        {F ⊃ K, F ⊃ A, ¬A} |- ¬F
        """
        model = Model(['(F >> K)', '(K >> A)', '~A'], '~F')
        result = Solver.solve(model)
        successful = result[0]
        proving_theory_list = result[1]
        print(proving_theory_list)
        self.assertTrue(successful)
        self.assertIn('~F', proving_theory_list[len(proving_theory_list)-1])

    def test_task_3(self) -> None:
        """
        Trying to prove the task below.
        Task:
        {¬(A ⊃ (B ⊃ C)), A ⊃ C} |- B
        """
        model = Model(['~(A >> (B >> C))', '(A >> C)', ], 'B')
        result = Solver.solve(model)
        successful = result[0]
        proving_theory_list = result[1]
        print(proving_theory_list)
        self.assertTrue(successful)
        self.assertIn('B', proving_theory_list[len(proving_theory_list)-1])

    def test_task_4(self) -> None:
        """
        Trying to prove the task below.
        Task:
        {¬(A ∨ (B ⊃ B)), A ⊃ B} |- C
        """
        model = Model(['~(A | (B >> B))', '(A >> B)', ], 'C')
        result = Solver.solve(model)
        successful = result[0]
        proving_theory_list = result[1]
        print(proving_theory_list)
        self.assertTrue(successful)
        self.assertIn('C', proving_theory_list[len(proving_theory_list)-1])


if __name__ == '__main__':
    unittest.main()
