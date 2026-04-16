from __future__ import annotations
from game.major_game_classes.character_related.Person_ren import Person
"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init -2 python:
"""

day = 0

# One in-game year is 12 months of 30 days each.
_DAYS_PER_YEAR: int = 360

class Kid:
    '''
    Records a child born to a :class:`Person` during the game.

    Fields
    ------
    first_name : str
        The child's given name.
    last_name : str
        The child's family name (typically inherited from the mother).
    birthdate : int
        The in-game day on which the child was born.
    gender : str
        ``"female"`` or ``"male"``.
    mother : Person
        Direct reference to the :class:`Person` who gave birth.
    father : str
        Name of the acknowledged / legal father, or ``"Unknown"``.
    bio_father : str
        Name of the biological father, or ``"Unknown"``.
        Matches *father* unless there is a known discrepancy.

    Computed properties
    -------------------
    age : int
        Years elapsed since *birthdate*, based on 360 game-days per year.
    full_name : str
        ``"<first_name> <last_name>"``.
    '''

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birthdate: int,
        gender: str,
        mother: Person,
        father: str,
        bio_father: str,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.gender = gender
        self.mother = mother
        self.father = father
        self.bio_father = bio_father

    # ------------------------------------------------------------------
    # Helper properties
    # ------------------------------------------------------------------

    @property
    def age(self) -> int:
        '''Years old, calculated from *birthdate* and the current game *day*.'''
        return (day - self.birthdate) // _DAYS_PER_YEAR

    @property
    def full_name(self) -> str:
        '''``"<first_name> <last_name>"``.'''
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return f"Kid({self.full_name!r}, gender={self.gender!r}, age={self.age})"
