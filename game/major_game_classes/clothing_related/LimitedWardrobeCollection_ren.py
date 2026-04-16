from __future__ import annotations
from collections.abc import Iterator
from typing import Iterable
from game.bugfix_additions.debug_info_ren import write_log
from game.major_game_classes.character_related.Person_ren import Person
from game.major_game_classes.clothing_related.LimitedWardrobe_ren import LimitedWardrobe
from game.major_game_classes.clothing_related.Outfit_ren import Outfit

limited_wardrobes: LimitedWardrobeCollection
"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init -3 python:
"""
from collections import UserList

class LimitedWardrobeCollection(UserList):
    def __init__(self, iterable = None):
        if iterable is None:
            iterable = []
        super().__init__(item for item in iterable if type(item) in [LimitedWardrobe])
        self._update_sorted_list()

    def __setstate__(self, state):
        '''Rebuild _sorted after deserialization to prevent stale ordering.'''
        self.__dict__.update(state)
        self._update_sorted_list()

    def __setitem__(self, index, item):
        if type(item) in [LimitedWardrobe]:
            self.data[index] = item
        else:
            msg = 'Item must be a limited wardrobe.'
            raise TypeError(msg)

    def _update_sorted_list(self):
        self._sorted = sorted(self.data, key=lambda x: x.priority, reverse=True)

    def append(self, item: LimitedWardrobe):
        if type(item) in [LimitedWardrobe]:
            self.data.append(item)
            self._update_sorted_list()
        else:
            msg = 'Item must be a limited wardrobe.'
            raise TypeError(msg)

    def extend(self, items: Iterable[LimitedWardrobe]) -> None:
        self.data.extend(items)
        self._update_sorted_list()

    def __iter__(self) -> Iterator[LimitedWardrobe]:
        if not self._sorted and self.data:
            self._update_sorted_list()
        return iter(self._sorted)

    def reload_wardrobes(self):
        '''Reload all limited wardrobes from their XML files to pick up content changes.
        Also clears daily outfit caches and rebuilds the priority-sorted list.'''
        for wardrobe in self.data:
            if hasattr(wardrobe, '_wardrobe') and hasattr(wardrobe._wardrobe, 'filename') and wardrobe._wardrobe.filename:
                wardrobe._wardrobe.reload()
            if hasattr(wardrobe, 'daily_outfits'):
                wardrobe.daily_outfits.clear()
        self._update_sorted_list()

    def rebuild(self):
        '''Rebuild priority-sorted list and clear daily outfit caches without reloading XML.
        Use this to fix stale ordering or cached outfits after save/load.'''
        for wardrobe in self.data:
            if hasattr(wardrobe, 'daily_outfits'):
                wardrobe.daily_outfits.clear()
        self._update_sorted_list()

    def should_use_limited_wardrobe(self, person: Person) -> bool:
        for x in self:
            if x.has_outfits and x.is_valid(person):
                write_log("[LimitedWardrobeCollection.should_use] %s: YES matched '%s' (prio=%d)",
                          person.name, x.wardrobe.name, x.priority)
                return True
        return False

    def decide_on_outfit(self, person: Person, sluttiness_modifier: float = 0, slut_limit: int = 999, allow_personal_wardrobe = True) -> Outfit:
        limited_wardobe = next((x for x in self if x.has_outfits and x.is_valid(person)), None)
        if limited_wardobe is None:
            write_log("[LimitedWardrobeCollection.decide_on_outfit] %s: no matching limited wardrobe found", person.name)
            return None
        write_log("[LimitedWardrobeCollection.decide_on_outfit] %s: using '%s' (prio=%d) slut_mod=%.2f slut_limit=%d",
                  person.name, limited_wardobe.wardrobe.name, limited_wardobe.priority, sluttiness_modifier, slut_limit)
        return limited_wardobe.decide_on_outfit(person, sluttiness_modifier, slut_limit, allow_personal_wardrobe)

    def update_outfit(self, person: Person, outfit: Outfit):
        limited_wardobe = next((x for x in self if x.has_outfits and x.is_valid(person)), None)
        if limited_wardobe is None:
            return
        limited_wardobe.set_outfit(person, outfit)
