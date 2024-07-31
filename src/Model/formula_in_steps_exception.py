class FormulaInStepsException(Exception):
    """
    This exception raised, when the current formula that will be appended to the steps, currently in
    the steps.
    """
    def __init__(self) -> None:
        """
        Constructor of the exception.
        """
        super().__init__('Formula appears in the proving theory!')
