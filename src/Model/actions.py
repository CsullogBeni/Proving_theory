from enum import Enum


class Actions(Enum):
    """
    Enum for step Action. Representing a type of action in proving theory.
    HYP: using hypothesis
    AXIOM: using axiom
    MP: execute Modus Ponens rule
    MT: execute Modus Tollens rule
    MTP: execute Modus Tollendo Ponens rule
    MPT: execute Modus Ponendo Tollens rule
    CS: execute Conditional Syllogism rule
    """
    HYP = 0
    AXIOM = 1
    MP = 2
    MT = 3
    MTP = 4
    MPT = 5
    CS = 6
