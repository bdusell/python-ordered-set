import collections
import itertools
from collections.abc import Set, MutableSet
from typing import TypeVar

T = TypeVar('T')

_DUMMY_VALUE = None

class OrderedSet(MutableSet[T]):

    def __init__(self, values=()):
        super().__init__()
        self.dict = collections.OrderedDict.fromkeys(value, _DUMMY_VALUE)

    def add(self, item):
        self.dict[item] = _DUMMY_VALUE

    def discard(self, item):
        self.dict.pop(item, None)

    def update(self, other):
        for item in other:
            self.add(item)

    def remove(self, item):
        del self.dict[item]

    def isdisjoint(self, other):
        return not any(x in self for x in other)

    def issubset(self, other):
        return all(x in other for x in self)

    def __repr__(self):
        return f'OrderedSet({list(self)!r})'

    def __iter__(self):
        return iter(self.dict.keys())

    def __len__(self):
        return len(self.dict)

    def __or__(self, other):
        return OrderedSet(itertools.chain(self, other))

    def __contains__(self, item):
        return item in self.dict

class FrozenOrderedSet(Set[T]):

    def __init__(self, values):
        super().__init__()
        value_set = set()
        value_list = []
        for value in values:
            if value not in value_set:
                value_set.add(value)
                value_list.append(value)
        self.set = frozenset(value_set)
        self.list = value_list

    def isdisjoint(self, other):
        return not any(x in self for x in other)

    def issubset(self, other):
        return all(x in other for x in self)

    def __repr__(self):
        return f'FrozenOrderedSet({self.list!r})'

    def __iter__(self):
        return iter(self.list)

    def __len__(self):
        return len(self.list)

    def __contains__(self, item):
        return item in self.set

    def __hash__(self):
        return hash(self.set)

    def __eq__(self, other):
        return type(self) is type(other) and self.set == other.set
