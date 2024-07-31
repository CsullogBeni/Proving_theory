import json
import os.path


class AxiomReader:
    """
    AxiomReader class is for reading axioms, from axioms.json file.

    Attributes:
        __file_path: (str) path to tha json file, this class requires axioms.json file beside this class file.

    """
    def __init__(self) -> None:
        """
        Constructor to AxiomReader.
        """
        self.__file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'axioms.json')

    def read_axioms_from_json(self) -> list:
        """
        Reads axioms from the axioms.json file 'axioms' column.

        Raises
            FileNotFoundException
            json.JSONDecodeError

        Returns
            list of axioms read from json: Whether a file is not found, cannot be decoded, or there is no 'axioms'
            column, this returns [].
        """
        try:
            with open(self.__file_path, 'r') as file:
                data = json.load(file)
                if 'axioms' in data:
                    return data['axioms']
                else:
                    return []
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
