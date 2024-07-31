import os
import shutil
import json


class DataAccess:
    """
    Handles all file operations. Saving or loading windows, model's data. Handles the database.
    
    Attributes:
        __persistence_path: (str) contains the full path to Persistence directory
    """
    def __init__(self) -> None:
        self.__persistence_path = os.path.dirname(os.path.abspath(__file__))

    def __get_windows_persistence_path(self) -> str:
        """
        Returns path where all files stored

        Raises:
            OSError if path does not exist

        Returns
            \\Persistence\\Windows\\ dir full path
        """
        try:
            windows_path = os.path.join(self.__persistence_path, 'Windows')
            return windows_path
        except Exception:
            raise OSError

    def __get_saves_persistence_path(self) -> str:
        """
        Returns path where all files stored

        Raises
            OSError if path does not exist

        Returns
            \\Persistence\\Saves\\ dir full path
        """
        try:
            saves_path = os.path.join(self.__persistence_path, 'Saves')
            return saves_path
        except Exception:
            raise OSError

    def windows_cleaner(self) -> None:
        """
        Delete all files in Persistence\\Windows directory.

        Raises
            OSError if path does not exist
        """
        try:
            persistence_path = self.__get_windows_persistence_path()
            shutil.rmtree(persistence_path)
            os.makedirs(persistence_path)
        except Exception:
            raise OSError

    def save_new_proving_method_config_window(self,
                                              formula_set: list,
                                              consequence_formula: str) -> None:
        """
        If new_proving_method_config_window.json exists, delete the file.
        Save formula_list and consequence_formula in a new_proving_method_config_window.json file.

        Args:
            formula_set: list of valid logical formulas.
            consequence_formula: consequence formula

        Raises:
            OSError
        """
        try:
            persistence = self.__get_windows_persistence_path()
        except OSError:
            raise OSError

        file_path = os.path.join(persistence, 'new_proving_method_config_window.json')
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                raise OSError

        data = {
            'formula_set': formula_set,
            'consequence_formula': consequence_formula
        }

        try:
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=2)
                json_file.close()
        except Exception:
            raise OSError

    def load_new_proving_method_config_window(self) -> (list, str):
        """
        Reads \\Persistence\\Windows\\new_proving_method_config_window.json

        Raises:
            OSError

        Returns
            formula_set (str list), consequence_formula (str)
        """
        try:
            persistence = self.__get_windows_persistence_path()
        except OSError:
            raise OSError

        file_path = os.path.join(persistence, 'new_proving_method_config_window.json')

        try:
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                formula_set = data['formula_set']
                consequence_formula = data['consequence_formula']
                json_file.close()
        except Exception:
            raise OSError

        return formula_set, consequence_formula

    def save_loading_window(self, model_path: str) -> None:
        """
        If loading_window.json exists, delete the file.
        Save model_path in a loading_window.json file.

        Raises:
            OSError

        Args:
            model_path: model path contains a full path to a json file, that contains all data for
            model object
        """
        try:
            persistence = self.__get_windows_persistence_path()
        except OSError:
            raise OSError

        file_path = os.path.join(persistence, 'loading_window.json')
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                raise OSError

        data = {
            'file_path': model_path
        }

        try:
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=2)
                json_file.close()
        except Exception:
            raise OSError

    def load_loading_window(self) -> str:
        """
        Reads \\persistence\\Windows\\loading_window.json

        Raises:
            OSError
        Returns:
            model_path (str): full path to a json file, that contains data for model
        """
        try:
            persistence = self.__get_windows_persistence_path()
        except OSError:
            raise OSError

        file_path = os.path.join(persistence, 'loading_window.json')

        try:
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                json_file.close()
        except Exception:
            raise OSError

        return data['file_path']

    def save_model(self, data: dict) -> None:
        """
        Function saves all data of a model to a json file. Name of the json file contains the current datetime.
        File saved in Persistence\\Saves\\ folder.

        Raises:
            OSError

        Args:
            data: dictionary contains all data of the model, that calls this function
        """
        from datetime import datetime
        try:
            persistence = self.__get_saves_persistence_path()
        except Exception:
            raise OSError

        now = datetime.now()
        file = now.strftime("%Y-%m-%d_%H-%M") + '.json'

        path = os.path.join(persistence, file)

        if os.path.exists(path):
            raise OSError

        try:
            with open(path, 'w') as f:
                json.dump(data, f)
                f.close()
        except Exception:
            raise OSError

    @staticmethod
    def load_model(path: str) -> dict:
        """
        Read all data from the given file to a dictionary.

        Raises:
            OSError

        Args:
            path: path to the json file, that contains all data

        Returns:
            Dictionary that contains all data for a model
        """
        try:
            with open(path) as f:
                data = json.load(f)
                f.close()
        except OSError:
            raise OSError
        except Exception:
            raise OSError
        return data

    def model_list(self) -> list:
        """
        Run through tha saves directory in Persistence. THe directory contains every save of model.
        Function lists all saves, and gives full path to the saves.

        Raises:
            OSError

        Returns:
            list of tuple. a tuple contains the file path and a string that represents the datetime and the task
            (formula_set, consequence_formula concat).
        """
        try:
            persistence = self.__get_saves_persistence_path()
        except Exception:
            raise OSError

        paths_names = []
        try:
            for file in os.listdir(persistence):
                try:
                    full_path = os.path.join(persistence, file)
                    data = self.load_model(full_path)
                    generated_file_name = data['task_name'] + ' - ' + file[:-5]
                    paths_names.append((full_path, generated_file_name))
                except OSError:
                    continue
        except:
            raise OSError
        return paths_names
