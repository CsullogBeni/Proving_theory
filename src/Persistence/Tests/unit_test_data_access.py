import unittest
import os
import json

from Persistence.data_access import DataAccess


class UnitTestUtils(unittest.TestCase):
    """
    Unit test for Persistence.Utils.utils.py
    Testing helper functions.
    """

    def test_windows_cleaner(self) -> None:
        """
        Unit tests for Persistence.Utils.utils.windows_cleaner function
        """
        persistence_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        persistence_path = os.path.join(persistence_path, 'Windows')
        data_access = DataAccess()
        data_access.windows_cleaner()
        self.assertTrue(os.path.exists(persistence_path))
        self.assertTrue(len(os.listdir(persistence_path)) == 0)

    def test_save_new_proving_method_config_window(self) -> None:
        """
        Unit tests for Persistence.Utils.utils.save_new_proving_method_config_window function
        """
        data_access = DataAccess()
        data_access.save_new_proving_method_config_window(['(A >> B)', 'A'], 'B')
        persistence_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        persistence_path = os.path.join(persistence_path, 'Windows')
        persistence_path = os.path.join(persistence_path, 'new_proving_method_config_window.json')
        self.assertTrue(os.path.exists(persistence_path))
        with open(persistence_path, 'r') as json_file:
            data = json.load(json_file)
            formula_set = data['formula_set']
            consequence_formula = data['consequence_formula']
        self.assertTrue(formula_set == ['(A >> B)', 'A'])
        self.assertTrue(consequence_formula == 'B')

    def test_load_new_proving_method_config_window(self) -> None:
        """
        Unit tests for Persistence.Utils.utils.load_new_proving_method_config_function function
        """
        data_access = DataAccess()
        persistence = data_access._DataAccess__get_windows_persistence_path()
        file_path = os.path.join(persistence, 'new_proving_method_config_window.json')
        data = {
            'formula_set': ['(A >> B)', 'A'],
            'consequence_formula': 'B'
        }
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        self.assertTrue(os.path.exists(file_path))
        data_access = DataAccess()
        self.assertTrue(data_access.load_new_proving_method_config_window() == (['(A >> B)', 'A'], 'B'))

    def test_save_model(self) -> None:
        """
        Unit tests for Persistence.Utils.utils.save_model function
        """
        from datetime import datetime
        data_access = DataAccess()
        data = {
            'formula_set': ['A', 'B'],
            'consequence_formula': 'C',
            'end': False,
            'number_of_steps': 1,
            'steps': [[0, 'A', 'Actions.HYP', "", 0, 0]],
            'task_name': '{A, B} |- C',
            "added_axioms": []
        }
        data_access.save_model(data)

        persistence = data_access._DataAccess__get_saves_persistence_path()
        now = datetime.now()
        file = now.strftime("%Y-%m-%d_%H-%M") + '.json'
        path = os.path.join(persistence, file)
        with open(path) as f:
            read_data = json.load(f)
            f.close()
        self.assertEqual(data, read_data)

    def test_load_model(self) -> None:
        """
        Unit tests for Persistence.Utils.utils.load_model function
        """
        data = {
            'formula_set': ['A', 'B'],
            'consequence_formula': 'C',
            'end': False,
            'number_of_steps': 1,
            'steps': [[0, 'A', 'Actions.HYP', "", 0, 0]],
            'task_name': '{A, B} |- C',
            "added_axioms": []
        }
        data_access = DataAccess()
        persistence = data_access._DataAccess__get_saves_persistence_path()
        path = os.path.join(persistence, 'test.json')
        with open(path, 'w') as f:
            json.dump(data, f)
            f.close()
        data_access = DataAccess()
        read_data = data_access.load_model(path)
        self.assertEqual(data, read_data)


if __name__ == "__main__":
    unittest.main()
