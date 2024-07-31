class TaskIsNotProvableException(Exception):
    """
    This exception raised, when the conclusion can't be proven.
    """
    def __init__(self):
        """
        Constructor of the exception.
        """
        super().__init__('Task is not provable!')
