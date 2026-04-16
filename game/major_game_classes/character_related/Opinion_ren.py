from __future__ import annotations
from typing import Iterable
from game.major_game_classes.character_related.Person_ren import Person

"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init -5 python:
"""

class Opinion():
    # Maps attribute names whose topic strings cannot be derived by a simple
    # underscore-to-space conversion.
    _TOPIC_MAP = {
        "doggy_style": "doggy style sex",
        "missionary_style": "missionary style sex",
        "hr_work": "HR work",
    }

    def __init__(self, person: Person, known = False):
        self.person = person
        if known:
            self.get_func = self.person.get_known_opinion_score
        else:
            self.get_func = self.person.get_opinion_score

    def __hash__(self) -> int:
        return hash(self.person)

    def __eq__(self, other: Opinion) -> bool:
        if not isinstance(other, Opinion):
            return NotImplemented
        return self.person == other.person

    def __call__(self, topic: str | Iterable[str]) -> int:
        '''
        Default callable object for undefined topics
        When topic is iterable[str] sums the passed opinions scores and returns that value
        '''
        if isinstance(topic, str):
            return self.get_func(topic)

        value = 0
        for x in (x for x in topic if isinstance(x, str)):
            value += self.get_func(x)
        return value

    def __getattr__(self, name: str) -> int:
        '''
        Looks up an opinion topic by attribute name.
        The topic string is derived by replacing underscores with spaces, with
        special-case overrides stored in _TOPIC_MAP for names that don't follow
        that simple pattern.
        '''
        if name.startswith('_'):
            raise AttributeError(name)
        topic = self._TOPIC_MAP.get(name, name.replace("_", " "))
        # Use object.__getattribute__ to avoid recursive __getattr__ calls if
        # get_func itself is not yet set (e.g. during unpickling).
        get_func = object.__getattribute__(self, 'get_func')
        return get_func(topic)
